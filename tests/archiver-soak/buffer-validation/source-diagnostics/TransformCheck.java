import java.lang.instrument.ClassFileTransformer;
import java.lang.reflect.Constructor;
import java.nio.file.Files;
import java.nio.file.Path;
import jdk.internal.org.objectweb.asm.ClassReader;
import jdk.internal.org.objectweb.asm.ClassVisitor;
import jdk.internal.org.objectweb.asm.MethodVisitor;
import jdk.internal.org.objectweb.asm.Opcodes;

/** Verifies observer insertion against actual installed class bytes and the JVM verifier. */
public final class TransformCheck {
    private static final String[] TARGETS = {
        "org/epics/archiverappliance/engine/writer/WriterRunnable",
        "org/epics/archiverappliance/engine/model/SampleBuffer",
        "edu/stanford/slac/archiverappliance/PlainPB/AppendDataStateData"
    };

    private static final class VerificationLoader extends ClassLoader {
        VerificationLoader() { super(TransformCheck.class.getClassLoader()); }
        Class<?> verify(String name, byte[] bytes) {
            Class<?> type = defineClass(name.replace('/', '.'), bytes, 0, bytes.length);
            resolveClass(type);
            type.getDeclaredMethods();
            return type;
        }
    }

    public static void main(String[] args) throws Exception {
        Constructor<?> constructor = Class.forName("buffer29.Agent$Observer").getDeclaredConstructor();
        constructor.setAccessible(true);
        ClassFileTransformer observer = (ClassFileTransformer) constructor.newInstance();
        int[] callbacks = new int[4];
        for (String target : TARGETS) {
            byte[] original = Files.readAllBytes(Path.of(args[0], target + ".class"));
            byte[] transformed = observer.transform(TransformCheck.class.getClassLoader(), target, null, null, original);
            if (transformed == null) throw new IllegalStateException("Missing transformed class");
            new ClassReader(transformed).accept(new ClassVisitor(Opcodes.ASM8) {
                @Override
                public MethodVisitor visitMethod(int access, String method, String descriptor,
                                                 String signature, String[] exceptions) {
                    return new MethodVisitor(Opcodes.ASM8) {
                        private int previousOpcode = -1;
                        @Override
                        public void visitInsn(int opcode) { previousOpcode = opcode; }
                        @Override
                        public void visitMethodInsn(int opcode, String owner, String name, String desc, boolean itf) {
                            if (owner.equals("buffer29/Trace")) {
                                if (name.equals("begin")) callbacks[0]++;
                                if (name.equals("input")) callbacks[1]++;
                                if (name.equals("swap")) callbacks[2]++;
                                if (name.equals("flush") && previousOpcode == Opcodes.ICONST_1) callbacks[3]++;
                            }
                            previousOpcode = -1;
                        }
                    };
                }
            }, 0);
            new VerificationLoader().verify(target, transformed);
        }
        for (int count : callbacks) if (count != 1) throw new IllegalStateException("Unexpected observer insertion count");
        System.out.println("Verified three actual installed classes; exactly one final-flush entry marker");
    }
}
