package buffer29;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.IdentityHashMap;
import java.util.Set;

/** Captures independent pre-buffer inputs and the real per-buffer counters. */
public final class Trace {
    private static Set<String> fast = Set.of();
    private static volatile boolean failed;
    private static final IdentityHashMap<Object, Long> identities = new IdentityHashMap<>();

    private static synchronized long identity(Object buffer) {
        return identities.computeIfAbsent(buffer, key -> (long) identities.size() + 1);
    }

    private record BufferFields(Field name, Field capacity, Field metrics, Field lost) {}
    private record EventMethods(Method raw, Method seconds) {}
    private record RawFields(Field bytes, Field offset, Field length) {}

    private static Field field(Class<?> type, String name) throws Exception {
        Field value = type.getDeclaredField(name);
        value.setAccessible(true);
        return value;
    }

    private static final ClassValue<BufferFields> BUFFERS = new ClassValue<>() {
        @Override
        protected BufferFields computeValue(Class<?> type) {
            try {
                Field metrics = field(type, "pVMetrics");
                return new BufferFields(field(type, "channel_name"), field(type, "capacity"),
                        metrics, field(metrics.getType(), "sampleBufferFullLostEventCount"));
            } catch (Exception error) {
                throw new IllegalStateException(error);
            }
        }
    };

    private static final ClassValue<EventMethods> EVENTS = new ClassValue<>() {
        @Override
        protected EventMethods computeValue(Class<?> type) {
            try {
                return new EventMethods(type.getMethod("getRawForm"), type.getMethod("getEpochSeconds"));
            } catch (Exception error) {
                throw new IllegalStateException(error);
            }
        }
    };

    private static final ClassValue<RawFields> RAW = new ClassValue<>() {
        @Override
        protected RawFields computeValue(Class<?> type) {
            try {
                return new RawFields(type.getField("data"), type.getField("off"), type.getField("len"));
            } catch (Exception error) {
                throw new IllegalStateException(error);
            }
        }
    };

    public static boolean initialize(String tools) {
        try {
            System.load(Path.of(tools, "libbuffer29.so").toString());
            fast = new HashSet<>(Files.readAllLines(Path.of(tools, "fast.txt")));
            if (fast.size() != 110) throw new IllegalStateException("Expected 110 fast PVs");
            Path output = Path.of(System.getProperty("buffer29.output"));
            Files.createDirectories(output);
            return configure(output.toString()) == 0;
        } catch (Throwable error) {
            failed = true;
            System.err.println("BUFFER29_AGENT_ERROR " + error.getClass().getName());
            return false;
        }
    }

    private static void failure(Throwable error) {
        if (failed) return;
        failed = true;
        System.err.println("BUFFER29_AGENT_ERROR " + error.getClass().getName());
        try {
            errorNative(error.getClass().getName());
        } catch (Throwable ignored) {
            System.err.println("BUFFER29_NATIVE_ERROR");
        }
    }

    public static void input(Object buffer, Object event) {
        if (failed) return;
        try {
            BufferFields fields = BUFFERS.get(buffer.getClass());
            String name = (String) fields.name().get(buffer);
            long lost = fields.lost().getLong(fields.metrics().get(buffer));
            int capacity = fields.capacity().getInt(buffer);
            if (!fast.contains(name)) {
                inputNative(name, null, 0, 0, 0, capacity, lost, identity(buffer));
                return;
            }
            EventMethods methods = EVENTS.get(event.getClass());
            Object raw = methods.raw().invoke(event);
            RawFields bytes = RAW.get(raw.getClass());
            inputNative(name, (byte[]) bytes.bytes().get(raw), bytes.offset().getInt(raw),
                    bytes.length().getInt(raw), (Long) methods.seconds().invoke(event), capacity, lost, identity(buffer));
        } catch (Throwable error) {
            failure(error);
        }
    }

    public static void swap(Object buffer) {
        if (failed) return;
        try {
            BufferFields fields = BUFFERS.get(buffer.getClass());
            swapNative((String) fields.name().get(buffer), fields.capacity().getInt(buffer),
                    fields.lost().getLong(fields.metrics().get(buffer)), identity(buffer));
        } catch (Throwable error) {
            failure(error);
        }
    }

    public static void begin(Object writer) {
        if (failed) return;
        try {
            Object service = field(writer.getClass(), "configservice").get(writer);
            Object context = service.getClass().getMethod("getEngineContext").invoke(service);
            double period = (Double) context.getClass().getMethod("getWritePeriod").invoke(context);
            double margin = (Double) context.getClass().getMethod("getSampleBufferMarginSeconds").invoke(context);
            configurationNative(period, margin);
            beginNative();
        } catch (Throwable error) {
            failure(error);
        }
    }

    public static void end() {
        if (failed) return;
        try {
            endNative();
        } catch (Throwable error) {
            failure(error);
        }
    }

    public static void flush(boolean active) {
        if (failed) return;
        try {
            flushNative(active);
        } catch (Throwable error) {
            failure(error);
        }
    }

    private static native int configure(String output);
    private static native void inputNative(String name, byte[] data, int offset, int length,
                                          long seconds, int capacity, long lost, long identity);
    private static native void swapNative(String name, int capacity, long lost, long identity);
    private static native void beginNative();
    private static native void endNative();
    private static native void configurationNative(double period, double margin);
    private static native void flushNative(boolean active);
    private static native void errorNative(String message);
}
