import edu.stanford.slac.archiverappliance.PlainPB.FileBackedPBEventStream;
import edu.stanford.slac.archiverappliance.PlainPB.PlainPBPathNameUtility;
import edu.stanford.slac.archiverappliance.PlainPB.PlainPBStoragePlugin;
import org.epics.archiverappliance.ByteArray;
import org.epics.archiverappliance.Event;
import org.epics.archiverappliance.common.BasicContext;
import org.epics.archiverappliance.common.POJOEvent;
import org.epics.archiverappliance.common.TimeUtils;
import org.epics.archiverappliance.config.ArchDBRTypes;
import org.epics.archiverappliance.config.ConfigServiceForTests;
import org.epics.archiverappliance.config.ConvertPVNameToKey;
import org.epics.archiverappliance.config.DefaultConfigService;
import org.epics.archiverappliance.config.PVNameToKeyMapping;
import org.epics.archiverappliance.config.StoragePluginURLParser;
import org.epics.archiverappliance.data.AlarmInfo;
import org.epics.archiverappliance.data.ScalarValue;
import org.epics.archiverappliance.engine.membuf.ArrayListEventStream;
import org.epics.archiverappliance.retrieval.RemotableEventStreamDesc;
import org.epics.archiverappliance.utils.nio.ArchPaths;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import gov.aps.jca.Channel;
import gov.aps.jca.Context;
import gov.aps.jca.JCALibrary;
import gov.aps.jca.configuration.DefaultConfiguration;
import gov.aps.jca.dbr.DBRType;
import gov.aps.jca.dbr.DBR_TIME_Double;

import java.nio.file.Files;
import java.nio.file.Path;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Arrays;
import java.util.Base64;
import java.util.ArrayList;

/** Seeds and decodes real PB files; never invokes ETL or the appliance scheduler. */
public class PBFixture {
    private static final ArchDBRTypes TYPE = ArchDBRTypes.DBR_SCALAR_DOUBLE;
    private static final int MAX_SNAPSHOT_WINDOWS = 8;
    private static final long MAX_SNAPSHOT_WINDOW_SECONDS = 300;
    private static final double CA_TIMEOUT_SECONDS = 5.0;

    @SuppressWarnings("unchecked")
    private static JSONObject caSamples(JSONObject manifest) throws Exception {
        DefaultConfiguration configuration = new DefaultConfiguration("context");
        configuration.setAttribute("class", JCALibrary.CHANNEL_ACCESS_JAVA);
        configuration.setAttribute("addr_list", "127.0.0.1");
        configuration.setAttribute("auto_addr_list", "false");
        Context context = JCALibrary.getInstance().createContext(configuration);
        JSONObject output = new JSONObject();
        try {
            for (Object object : (JSONArray) manifest.get("pvs")) {
                JSONObject entry = (JSONObject) object;
                String pv = (String) entry.get("pv");
                Channel channel = context.createChannel(pv);
                try {
                    context.pendIO(CA_TIMEOUT_SECONDS);
                    DBR_TIME_Double value = (DBR_TIME_Double) channel.get(DBRType.TIME_DOUBLE, 1);
                    context.pendIO(CA_TIMEOUT_SECONDS);
                    Instant stamp = TimeUtils.convertFromJCATimeStamp(value.getTimeStamp());
                    JSONObject sample = new JSONObject();
                    sample.put("secs", stamp.getEpochSecond());
                    sample.put("nanos", stamp.getNano());
                    sample.put("val", value.getDoubleValue()[0]);
                    sample.put("status", value.getStatus().getValue());
                    sample.put("severity", value.getSeverity().getValue());
                    output.put(pv, sample);
                } finally {
                    channel.destroy();
                }
            }
        } finally {
            context.destroy();
        }
        return output;
    }

    private static String withRoot(String url, Path root) {
        int queryStart = url.indexOf('?');
        if (queryStart < 0) throw new IllegalArgumentException("Missing storage query");
        String[] fields = url.substring(queryStart + 1).split("&", -1);
        int replaced = 0;
        for (int index = 0; index < fields.length; index++) {
            String[] pair = fields[index].split("=", 2);
            if (URLDecoder.decode(pair[0], StandardCharsets.UTF_8).equals("rootFolder")) {
                fields[index] = pair[0] + "=" + URLEncoder.encode(root.toString(), StandardCharsets.UTF_8);
                replaced++;
            }
        }
        if (replaced != 1) throw new IllegalArgumentException("Expected one storage rootFolder");
        return url.substring(0, queryStart + 1) + String.join("&", fields);
    }

    private static int write(PlainPBStoragePlugin store, String pv, JSONArray samples, int from, int to) throws Exception {
        ArrayListEventStream stream = new ArrayListEventStream(to - from, new RemotableEventStreamDesc(TYPE, pv, TimeUtils.getCurrentYear()));
        for (int index = from; index < to; index++) {
            JSONObject sample = (JSONObject) samples.get(index);
            stream.add(new POJOEvent(TYPE, Instant.ofEpochSecond(((Number) sample.get("secs")).longValue(), ((Number) sample.get("nanos")).longValue()),
                    new ScalarValue<Double>(((Number) sample.get("val")).doubleValue()), ((Number) sample.get("status")).intValue(), ((Number) sample.get("severity")).intValue()));
        }
        try (BasicContext context = new BasicContext()) { return store.appendData(context, pv, stream); }
    }

    @SuppressWarnings("unchecked")
    private static JSONObject describe(Event event) {
        ByteArray raw = event.getRawForm();
        JSONObject result = new JSONObject();
        result.put("secs", event.getEventTimeStamp().getEpochSecond());
        result.put("nanos", event.getEventTimeStamp().getNano());
        result.put("raw", Base64.getEncoder().encodeToString(Arrays.copyOfRange(raw.data, raw.off, raw.off + raw.len)));
        result.put("val", Double.parseDouble(event.getSampleValue().toJSONString()));
        AlarmInfo alarm = (AlarmInfo) event;
        result.put("status", alarm.getStatus());
        result.put("severity", alarm.getSeverity());
        return result;
    }

    private static long[][] snapshotWindows(JSONObject entry) {
        JSONArray ranges = (JSONArray) entry.get("snapshot_windows");
        if (ranges == null || ranges.isEmpty() || ranges.size() > MAX_SNAPSHOT_WINDOWS) {
            throw new IllegalArgumentException("Bounded snapshot windows are required");
        }
        long[][] windows = new long[ranges.size()][2];
        for (int index = 0; index < ranges.size(); index++) {
            JSONArray range = (JSONArray) ranges.get(index);
            if (range.size() != 2) throw new IllegalArgumentException("Invalid snapshot window");
            windows[index][0] = ((Number) range.getFirst()).longValue();
            windows[index][1] = ((Number) range.getLast()).longValue();
            if (windows[index][1] <= windows[index][0]
                    || windows[index][1] - windows[index][0] > MAX_SNAPSHOT_WINDOW_SECONDS) {
                throw new IllegalArgumentException("Invalid snapshot window length");
            }
        }
        return windows;
    }

    private static boolean retain(Event event, long[][] windows) {
        long seconds = event.getEventTimeStamp().getEpochSecond();
        for (long[] window : windows) {
            if (window[0] <= seconds && seconds < window[1]) return true;
        }
        return false;
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] args) throws Exception {
        JSONObject manifest = (JSONObject) new JSONParser().parse(Files.readString(Path.of(args[1])));
        if (args[0].equals("keys")) {
            ConfigServiceForTests config = new ConfigServiceForTests(-1);
            try {
                config.getInstallationProperties().clear();
                try (var input = Files.newInputStream(Path.of(args[3]))) {
                    config.getInstallationProperties().load(input);
                }
                String className = config.getInstallationProperties().getProperty(
                        DefaultConfigService.ARCHAPPL_PVNAME_TO_KEY_MAPPING_CLASSNAME);
                PVNameToKeyMapping converter = className == null || className.isEmpty()
                        ? new ConvertPVNameToKey()
                        : (PVNameToKeyMapping) Class.forName(className).getConstructor().newInstance();
                converter.initialize(config);
                JSONObject keys = new JSONObject();
                for (Object object : (JSONArray) manifest.get("pvs")) {
                    String pv = (String) ((JSONObject) object).get("pv");
                    keys.put(pv, converter.convertPVNameToKey(pv));
                }
                Files.writeString(Path.of(args[2]), keys.toJSONString() + "\n");
            } finally {
                config.shutdownNow();
            }
            return;
        }
        if (args[0].equals("ca")) {
            Files.writeString(Path.of(args[2]), caSamples(manifest).toJSONString() + "\n");
            return;
        }
        if (!args[0].equals("seed") && !args[0].equals("snapshot")) {
            throw new IllegalArgumentException("Mode must be seed, snapshot or ca");
        }
        ConfigServiceForTests config = new ConfigServiceForTests(-1);
        JSONObject output = new JSONObject();
        int pvIndex = 0;
        try {
            for (Object object : (JSONArray) manifest.get("pvs")) {
                JSONObject entry = (JSONObject) object;
                long[][] windows = snapshotWindows(entry);
                String pv = (String) entry.get("pv");
                String key = config.getPVNameToKeyConverter().convertPVNameToKey(pv);
                if (entry.get("chunkKey") != null && !key.equals(entry.get("chunkKey"))) {
                    throw new IllegalStateException("Registered chunk key mismatch: " + pv);
                }
                JSONArray stores = (JSONArray) entry.get("stores");
                JSONArray created = new JSONArray();
                PlainPBStoragePlugin source = (PlainPBStoragePlugin) StoragePluginURLParser.parseStoragePlugin((String) stores.getFirst(), config);
                JSONArray destinations = new JSONArray();
                JSONArray input = (JSONArray) entry.get("input");
                for (int index = 0; index < input.size() - 1; index++) {
                    JSONObject sample = (JSONObject) input.get(index);
                    String destination = PlainPBPathNameUtility.getPathNameForTime(source, pv,
                            Instant.ofEpochSecond(((Number) sample.get("secs")).longValue(), ((Number) sample.get("nanos")).longValue()),
                            new ArchPaths(), config.getPVNameToKeyConverter()).toString();
                    if (!destinations.contains(destination)) destinations.add(destination);
                }
                output.put(pv + "#seedDestinations", destinations);
                PlainPBStoragePlugin mts = (PlainPBStoragePlugin) StoragePluginURLParser.parseStoragePlugin((String) stores.get(1), config);
                output.put(pv + "#oldMTSPath", PlainPBPathNameUtility.getPathNameForTime(mts, pv,
                        Instant.ofEpochSecond(((Number) entry.get("old")).longValue()), new ArchPaths(),
                        config.getPVNameToKeyConverter()).toString());
                if (args[0].equals("seed")) {
                    PlainPBStoragePlugin sts = (PlainPBStoragePlugin) StoragePluginURLParser.parseStoragePlugin((String) stores.getFirst(), config);
                    JSONArray samples = (JSONArray) entry.get("input");
                    Path staging = Path.of(args[2]).getParent().resolve("writer-staging").resolve("pv-" + pvIndex++).toAbsolutePath().normalize();
                    if (Files.exists(staging)) throw new IllegalStateException("Staging already exists: " + staging);
                    String stagingUrl = withRoot((String) stores.getFirst(), staging);
                    PlainPBStoragePlugin stagingStore = (PlainPBStoragePlugin) StoragePluginURLParser.parseStoragePlugin(stagingUrl, config);
                    Path resolvedStaging = Path.of(stagingStore.getRootFolder()).toAbsolutePath().normalize();
                    if (!resolvedStaging.equals(staging) || resolvedStaging.equals(Path.of(sts.getRootFolder()).toAbsolutePath().normalize())) {
                        throw new IllegalStateException("Staging must be separate from STS");
                    }
                    int historical = write(stagingStore, pv, samples, 0, samples.size() - 1);
                    if (historical != samples.size() - 1) throw new IllegalStateException("Incomplete historical writer input: " + pv);
                    Path[] stagedFiles = PlainPBPathNameUtility.getAllPathsForPV(new ArchPaths(), stagingStore.getRootFolder(), pv,
                            stagingStore.getExtensionString(), stagingStore.getPartitionGranularity(), PlainPBStoragePlugin.CompressionMode.NONE, config.getPVNameToKeyConverter());
                    for (Path stagedFile : stagedFiles) {
                        Path destination = Path.of(sts.getRootFolder()).resolve(staging.relativize(stagedFile));
                        if (Files.exists(destination)) throw new IllegalStateException("Historical partition already exists: " + destination);
                        ArrayList<Path> parents = new ArrayList<>();
                        for (Path parent = destination.getParent(); !Files.exists(parent); parent = parent.getParent()) parents.add(parent);
                        Files.createDirectories(destination.getParent());
                        Files.copy(stagedFile, destination);
                        for (Path parent : parents) created.add(parent.toString());
                        created.add(destination.toString());
                    }
                    JSONObject recentSample = (JSONObject) samples.getLast();
                    Path recentPath = PlainPBPathNameUtility.getPathNameForTime(sts, pv,
                            Instant.ofEpochSecond(((Number) recentSample.get("secs")).longValue(), ((Number) recentSample.get("nanos")).longValue()),
                            new ArchPaths(), config.getPVNameToKeyConverter());
                    boolean newRecentFile = !Files.exists(recentPath);
                    ArrayList<Path> recentParents = new ArrayList<>();
                    for (Path parent = recentPath.getParent(); !Files.exists(parent); parent = parent.getParent()) recentParents.add(parent);
                    int recent = write(sts, pv, samples, samples.size() - 1, samples.size());
                    if (recent != 1) throw new IllegalStateException("Incomplete recent writer input: " + pv);
                    for (Path parent : recentParents) created.add(parent.toString());
                    if (newRecentFile) created.add(recentPath.toString());
                    output.put(pv + "#seedAppended", historical + recent);
                    output.put(pv + "#createdPaths", created);
                }
                JSONArray pvStores = new JSONArray();
                for (Object url : stores) {
                    PlainPBStoragePlugin store = (PlainPBStoragePlugin) StoragePluginURLParser.parseStoragePlugin((String) url, config);
                    JSONArray files = new JSONArray();
                    Path[] paths = PlainPBPathNameUtility.getAllPathsForPV(new ArchPaths(), store.getRootFolder(), pv,
                            store.getExtensionString(), store.getPartitionGranularity(), PlainPBStoragePlugin.CompressionMode.NONE, config.getPVNameToKeyConverter());
                    for (Path path : paths) {
                        JSONObject file = new JSONObject();
                        file.put("path", path.toString());
                        JSONArray events = new JSONArray();
                        long decoded = 0;
                        try (var stream = new FileBackedPBEventStream(pv, path, TYPE)) {
                            for (Event event : stream) {
                                decoded++;
                                if (retain(event, windows)) events.add(describe(event));
                            }
                        }
                        file.put("decoded_events", decoded);
                        file.put("events", events);
                        files.add(file);
                    }
                    pvStores.add(files);
                }
                output.put(pv, pvStores);
            }
            Files.writeString(Path.of(args[2]), output.toJSONString() + "\n");
        } finally {
            config.shutdownNow();
        }
    }
}
