import edu.stanford.slac.archiverappliance.PB.data.PBScalarDouble;
import edu.stanford.slac.archiverappliance.PlainPB.FileBackedPBEventStream;
import edu.stanford.slac.archiverappliance.PlainPB.PBFileInfo;
import org.epics.archiverappliance.ByteArray;
import org.epics.archiverappliance.Event;
import org.epics.archiverappliance.config.ArchDBRTypes;
import org.epics.archiverappliance.data.DBRTimeEvent;

import java.io.BufferedInputStream;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.EOFException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/** Decodes captured inputs and preserved physical files with the shipped PB implementation. */
public final class PBDecode {
    private static final int HEADER_SIZE = 56;
    private static final int MAGIC = 0x42323931;
    private static final int INPUT = 1;
    private static final int PAYLOAD_LIMIT = 1048576;
    private record Physical(Path path, PBFileInfo info) {}

    private static void emit(BufferedWriter out, String pv, long arrival, Event event) throws Exception {
        if (event.getDBRType() != ArchDBRTypes.DBR_SCALAR_DOUBLE)
            throw new IllegalStateException("Unexpected fast event type");
        DBRTimeEvent timed = (DBRTimeEvent) event;
        long bits = Double.doubleToRawLongBits(event.getSampleValue().getValue().doubleValue());
        out.write(pv + "\t" + arrival + "\t" + event.getEpochSeconds() + "\t"
                + event.getEventTimeStamp().getNano() + "\t" + Long.toUnsignedString(bits) + "\t"
                + timed.getStatus() + "\t" + timed.getSeverity() + "\n");
    }

    private static void inputs(Path source, Path destination, Set<String> fast) throws Exception {
        try (DataInputStream in = new DataInputStream(new BufferedInputStream(Files.newInputStream(source)));
             BufferedWriter out = Files.newBufferedWriter(destination)) {
            while (true) {
                byte[] rawHeader = in.readNBytes(HEADER_SIZE);
                if (rawHeader.length == 0) break;
                if (rawHeader.length != HEADER_SIZE) throw new EOFException("Partial trace header");
                ByteBuffer h = ByteBuffer.wrap(rawHeader).order(ByteOrder.LITTLE_ENDIAN);
                if (h.getInt() != MAGIC) throw new IllegalStateException("Invalid trace magic");
                int type = Short.toUnsignedInt(h.getShort());
                int nameLength = Short.toUnsignedInt(h.getShort());
                int length = h.getInt();
                h.getInt();
                long arrival = h.getLong();
                h.getLong();
                h.getLong();
                long seconds = h.getLong();
                if (length < 0 || length > PAYLOAD_LIMIT || nameLength >= 512)
                    throw new IllegalStateException("Invalid trace lengths");
                byte[] nameBytes = in.readNBytes(nameLength);
                byte[] raw = in.readNBytes(length);
                if (nameBytes.length != nameLength || raw.length != length)
                    throw new EOFException("Partial trace record");
                String pv = new String(nameBytes, StandardCharsets.UTF_8);
                if (type != INPUT || !fast.contains(pv)) continue;
                if (raw.length == 0) throw new IllegalStateException("Missing actual input");
                short year = (short) Instant.ofEpochSecond(seconds).atZone(ZoneOffset.UTC).getYear();
                Event event = new PBScalarDouble(year, new ByteArray(raw));
                if (event.getEpochSeconds() != seconds) throw new IllegalStateException("Input year mismatch");
                emit(out, pv, arrival, event);
            }
        }
    }

    private static void physical(Path source, Path destination, Set<String> fast) throws Exception {
        List<Physical> files = new ArrayList<>();
        try (var paths = Files.walk(source)) {
            for (Path path : paths.filter(p -> p.toString().endsWith(".pb")).toList()) {
                PBFileInfo info = new PBFileInfo(path, false);
                if (!fast.contains(info.getPVName())) throw new IllegalStateException("Unexpected preserved PV");
                if (info.getType() != ArchDBRTypes.DBR_SCALAR_DOUBLE)
                    throw new IllegalStateException("Unexpected physical PB type");
                if (info.getFirstEvent() != null) files.add(new Physical(path, info));
            }
        }
        files.sort(Comparator.comparing((Physical f) -> f.info().getPVName())
                .thenComparing(f -> f.info().getFirstEvent().getEventTimeStamp())
                .thenComparing(f -> f.path().toString()));
        try (BufferedWriter out = Files.newBufferedWriter(destination)) {
            for (Physical file : files) {
                FileBackedPBEventStream stream = new FileBackedPBEventStream(
                        file.info().getPVName(), file.path(), file.info().getType());
                try {
                    for (Event event : stream) emit(out, file.info().getPVName(), 0, event);
                } finally {
                    stream.close();
                }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 4) throw new IllegalArgumentException("Expected mode source destination fast-list");
        Set<String> fast = new HashSet<>(Files.readAllLines(Path.of(args[3])));
        if (fast.size() != 110) throw new IllegalStateException("Expected 110 fast PVs");
        if (args[0].equals("inputs")) inputs(Path.of(args[1]), Path.of(args[2]), fast);
        else if (args[0].equals("physical")) physical(Path.of(args[1]), Path.of(args[2]), fast);
        else throw new IllegalArgumentException("Unknown mode");
    }
}
