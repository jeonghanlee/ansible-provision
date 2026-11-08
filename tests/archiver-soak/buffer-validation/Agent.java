package buffer29;

import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.Instrumentation;
import java.nio.file.Path;
import java.security.ProtectionDomain;
import java.util.jar.JarFile;
import jdk.internal.org.objectweb.asm.ClassReader;
import jdk.internal.org.objectweb.asm.ClassVisitor;
import jdk.internal.org.objectweb.asm.ClassWriter;
import jdk.internal.org.objectweb.asm.MethodVisitor;
import jdk.internal.org.objectweb.asm.Opcodes;
import jdk.internal.org.objectweb.asm.Type;
import jdk.internal.org.objectweb.asm.commons.AdviceAdapter;
import jdk.internal.org.objectweb.asm.commons.Method;

/** Observes shipped engine methods without replacing their implementation. */
public final class Agent {
    private static final String BUFFER = "org/epics/archiverappliance/engine/model/SampleBuffer";
    private static final String WRITER = "org/epics/archiverappliance/engine/writer/WriterRunnable";
    private static final String APPENDER = "edu/stanford/slac/archiverappliance/PlainPB/AppendDataStateData";
    private static final Type TRACE = Type.getObjectType("buffer29/Trace");

    public static void premain(String tools, Instrumentation instrumentation) throws Exception {
        instrumentation.appendToBootstrapClassLoaderSearch(
                new JarFile(Path.of(tools, "bootstrap.jar").toFile()));
        Class<?> trace = Class.forName("buffer29.Trace", true, null);
        boolean ready = (Boolean) trace.getMethod("initialize", String.class).invoke(null, tools);
        if (!ready) return;
        instrumentation.addTransformer(new Observer());
    }

    private static final class Observer implements ClassFileTransformer {
        @Override
        public byte[] transform(ClassLoader loader, String name, Class<?> previous,
                                ProtectionDomain domain, byte[] bytes) {
            if (!BUFFER.equals(name) && !WRITER.equals(name) && !APPENDER.equals(name)) return null;
            ClassReader reader = new ClassReader(bytes);
            ClassWriter output = new ClassWriter(reader, ClassWriter.COMPUTE_MAXS);
            reader.accept(new ClassVisitor(Opcodes.ASM8, output) {
                @Override
                public MethodVisitor visitMethod(int access, String method, String descriptor,
                                                 String signature, String[] exceptions) {
                    MethodVisitor original = super.visitMethod(access, method, descriptor, signature, exceptions);
                    boolean writer = WRITER.equals(name) && method.equals("run") && descriptor.equals("()V");
                    boolean swap = BUFFER.equals(name) && method.equals("resetSamples") && descriptor.equals("()V");
                    boolean input = BUFFER.equals(name) && method.equals("add")
                            && descriptor.equals("(Lorg/epics/archiverappliance/data/DBRTimeEvent;)Z");
                    boolean append = APPENDER.equals(name) && method.equals("partitionBoundaryAwareAppendData");
                    if (!writer && !swap && !input && !append) return original;
                    return new AdviceAdapter(Opcodes.ASM8, original, access, method, descriptor) {
                        private boolean finalCloseObserved;

                        @Override
                        public void visitMethodInsn(int opcode, String owner, String target,
                                                    String signature, boolean itf) {
                            boolean finalClose = append && !finalCloseObserved
                                    && owner.equals(APPENDER) && target.equals("closeStreams")
                                    && signature.equals("()V");
                            if (finalClose) {
                                finalCloseObserved = true;
                                push(true);
                                invokeStatic(TRACE, new Method("flush", "(Z)V"));
                            }
                            super.visitMethodInsn(opcode, owner, target, signature, itf);
                            if (finalClose) {
                                push(false);
                                invokeStatic(TRACE, new Method("flush", "(Z)V"));
                            }
                        }
                        @Override
                        protected void onMethodEnter() {
                            if (writer) {
                                loadThis();
                                invokeStatic(TRACE, new Method("begin", "(Ljava/lang/Object;)V"));
                            }
                            if (input) {
                                loadThis();
                                loadArg(0);
                                invokeStatic(TRACE, new Method("input", "(Ljava/lang/Object;Ljava/lang/Object;)V"));
                            }
                        }

                        @Override
                        protected void onMethodExit(int opcode) {
                            if (append) {
                                push(false);
                                invokeStatic(TRACE, new Method("flush", "(Z)V"));
                            }
                            if (opcode != RETURN) return;
                            if (writer) invokeStatic(TRACE, new Method("end", "()V"));
                            if (swap) {
                                loadThis();
                                invokeStatic(TRACE, new Method("swap", "(Ljava/lang/Object;)V"));
                            }
                        }
                    };
                }
            }, ClassReader.EXPAND_FRAMES);
            return output.toByteArray();
        }
    }
}
