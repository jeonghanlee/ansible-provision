#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <jni.h>
#include <limits.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/syscall.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#define RECORD_MAGIC 0x42323931U
#define NAME_LIMIT 512
#define PAYLOAD_LIMIT 1048576U
#define NANOSECONDS 1000000000ULL

enum record_type { INPUT = 1, SWAP, PASS_BEGIN, PASS_END, NATIVE_WRITE, INJECTION, READY,
                   ERROR_RECORD, CONFIGURATION, FINAL_FLUSH, IO_BOUNDARY };
enum phase_type { WARM = 0, BASE, LEVEL500, LEVEL800, EXPECT_LOSS, RECOVERY, FINISHED };

struct __attribute__((packed)) record_header {
    uint32_t magic;
    uint16_t type;
    uint16_t name_length;
    uint32_t payload_length;
    uint32_t capacity;
    uint64_t monotonic_ns;
    uint64_t pass;
    int64_t lost;
    uint64_t first;
    uint64_t second;
};

static int trace_fd = -1;
static char control_path[PATH_MAX];
static pthread_mutex_t trace_lock = PTHREAD_MUTEX_INITIALIZER;
static _Atomic int enabled;
static _Atomic int fatal_error;
static _Atomic uint64_t pass_sequence;
static uint64_t eligible_sequence;
static int control_used;

static __thread int active_pass;
static __thread int phase;
static __thread int injected;
static __thread int choose_first;
static __thread int final_flush;
static __thread uint64_t pass_id;
static __thread uint64_t requested_ns;
static __thread uint64_t native_writes;
static __thread uint64_t cycle;
static __thread char current_pv[NAME_LIMIT];
static __thread char previous_last[NAME_LIMIT];
static __thread char last_pv[NAME_LIMIT];
static __thread char selected_last[NAME_LIMIT];

static uint64_t monotonic_ns(void) {
    struct timespec value;
    clock_gettime(CLOCK_MONOTONIC, &value);
    return (uint64_t)value.tv_sec * NANOSECONDS + (uint64_t)value.tv_nsec;
}

static int write_all(int fd, const void *data, size_t length) {
    const unsigned char *bytes = data;
    while (length) {
        ssize_t written = syscall(SYS_write, fd, bytes, length);
        if (written < 0 && errno == EINTR) continue;
        if (written <= 0) return -1;
        bytes += written;
        length -= (size_t)written;
    }
    return 0;
}

static void record_event(int type, const char *name, const void *payload, uint32_t length,
                         uint32_t capacity, int64_t lost, uint64_t first, uint64_t second) {
    if (trace_fd < 0) return;
    size_t name_length = strlen(name);
    if (name_length >= NAME_LIMIT || length > PAYLOAD_LIMIT) {
        atomic_store(&fatal_error, 1);
        return;
    }
    struct record_header header = {
        RECORD_MAGIC, (uint16_t)type, (uint16_t)name_length, length, capacity,
        monotonic_ns(), active_pass ? pass_id : 0, lost, first, second
    };
    pthread_mutex_lock(&trace_lock);
    if (write_all(trace_fd, &header, sizeof(header)) || write_all(trace_fd, name, name_length)
            || (length && write_all(trace_fd, payload, length))) atomic_store(&fatal_error, 1);
    pthread_mutex_unlock(&trace_lock);
}

static void copy_name(char *destination, const char *source) {
    size_t length = strlen(source);
    if (length >= NAME_LIMIT) {
        atomic_store(&fatal_error, 1);
        destination[0] = 0;
        return;
    }
    memcpy(destination, source, length + 1);
}

JNIEXPORT jint JNICALL Java_buffer29_Trace_configure(JNIEnv *env, jclass cls, jstring output) {
    (void)cls;
    const char *directory = (*env)->GetStringUTFChars(env, output, NULL);
    if (!directory) return -1;
    char trace_path[PATH_MAX];
    int a = snprintf(trace_path, sizeof(trace_path), "%s/trace-%ld.bin", directory, (long)getpid());
    int b = snprintf(control_path, sizeof(control_path), "%s/control", directory);
    (*env)->ReleaseStringUTFChars(env, output, directory);
    if (a < 0 || (size_t)a >= sizeof(trace_path) || b < 0 || (size_t)b >= sizeof(control_path)) return -1;
    trace_fd = open(trace_path, O_WRONLY | O_CREAT | O_EXCL | O_CLOEXEC, 0600);
    if (trace_fd < 0) return -1;
    atomic_store(&enabled, 1);
    record_event(READY, "", NULL, 0, 0, 0, (uint64_t)getpid(), sizeof(struct record_header));
    return 0;
}

JNIEXPORT void JNICALL Java_buffer29_Trace_inputNative(JNIEnv *env, jclass cls, jstring pv,
        jbyteArray data, jint offset, jint length, jlong seconds, jint capacity, jlong lost, jlong identity) {
    (void)cls;
    const char *name = (*env)->GetStringUTFChars(env, pv, NULL);
    if (!name) return;
    unsigned char *payload = NULL;
    if (data && offset >= 0 && length > 0 && (uint32_t)length <= PAYLOAD_LIMIT
            && offset <= (*env)->GetArrayLength(env, data) - length) {
        payload = malloc((size_t)length);
        if (payload) (*env)->GetByteArrayRegion(env, data, offset, length, (jbyte *)payload);
    }
    if (data && (!payload || (*env)->ExceptionCheck(env))) {
        atomic_store(&fatal_error, 1);
    } else {
        record_event(INPUT, name, payload, payload ? (uint32_t)length : 0, (uint32_t)capacity,
                lost, (uint64_t)seconds, (uint64_t)identity);
    }
    free(payload);
    (*env)->ReleaseStringUTFChars(env, pv, name);
}

JNIEXPORT void JNICALL Java_buffer29_Trace_swapNative(JNIEnv *env, jclass cls, jstring pv,
                                                     jint capacity, jlong lost, jlong identity) {
    (void)cls;
    const char *name = (*env)->GetStringUTFChars(env, pv, NULL);
    if (!name) return;
    copy_name(current_pv, name);
    record_event(SWAP, name, NULL, 0, (uint32_t)capacity, lost, 0, (uint64_t)identity);
    (*env)->ReleaseStringUTFChars(env, pv, name);
}

JNIEXPORT void JNICALL Java_buffer29_Trace_beginNative(JNIEnv *env, jclass cls) {
    (void)env;
    (void)cls;
    active_pass = 1;
    pass_id = atomic_fetch_add(&pass_sequence, 1) + 1;
    native_writes = 0;
    injected = 0;
    final_flush = 0;
    requested_ns = 0;
    cycle = 0;
    phase = WARM;
    current_pv[0] = 0;
    last_pv[0] = 0;
    copy_name(selected_last, previous_last);
    char text[160] = {0};
    char mode[24] = {0};
    uint64_t origin = 0, deadline = 0;
    int fd = open(control_path, O_RDONLY | O_CLOEXEC);
    if (fd >= 0) {
        ssize_t length = read(fd, text, sizeof(text) - 1);
        close(fd);
        if (length > 0) sscanf(text, "%23s %lu %lu", mode, &origin, &deadline);
    }
    uint64_t now = monotonic_ns();
    if (!strcmp(mode, "base")) phase = BASE;
    if (!strcmp(mode, "p500")) phase = LEVEL500;
    if (!strcmp(mode, "p800")) phase = LEVEL800;
    if (!strcmp(mode, "control") && !control_used) phase = EXPECT_LOSS;
    if (!strcmp(mode, "main") && now >= origin && (!deadline || now < deadline)) {
        uint64_t elapsed = (now - origin) / NANOSECONDS;
        cycle = elapsed / 600 + 1;
        uint64_t position = elapsed % 600;
        phase = position < 60 ? BASE : position < 300 ? LEVEL500 : position < 540 ? LEVEL800 : RECOVERY;
    }
    if (deadline && now >= deadline) phase = FINISHED;
    if (phase == LEVEL500 || phase == LEVEL800) {
        requested_ns = phase == LEVEL500 ? 500000000ULL : 800000000ULL;
        choose_first = (++eligible_sequence % 2) != 0;
    } else if (phase == EXPECT_LOSS) {
        requested_ns = 1500000000ULL;
        choose_first = 1;
    }
    record_event(PASS_BEGIN, "", mode, (uint32_t)strlen(mode), (uint32_t)phase, 0, requested_ns, cycle);
}

JNIEXPORT void JNICALL Java_buffer29_Trace_endNative(JNIEnv *env, jclass cls) {
    (void)env;
    (void)cls;
    record_event(PASS_END, last_pv, NULL, 0, (uint32_t)phase,
            atomic_load(&fatal_error), native_writes, (uint64_t)injected);
    copy_name(previous_last, last_pv);
    active_pass = 0;
}

JNIEXPORT void JNICALL Java_buffer29_Trace_errorNative(JNIEnv *env, jclass cls, jstring message) {
    (void)cls;
    atomic_store(&fatal_error, 1);
    const char *text = (*env)->GetStringUTFChars(env, message, NULL);
    if (text) {
        record_event(ERROR_RECORD, "", text, (uint32_t)strlen(text), 0, 1, 0, 0);
        (*env)->ReleaseStringUTFChars(env, message, text);
    }
}

JNIEXPORT void JNICALL Java_buffer29_Trace_configurationNative(JNIEnv *env, jclass cls,
        jdouble period, jdouble margin) {
    (void)env;
    (void)cls;
    uint64_t period_bits, margin_bits;
    memcpy(&period_bits, &period, sizeof(period_bits));
    memcpy(&margin_bits, &margin, sizeof(margin_bits));
    record_event(CONFIGURATION, "", NULL, 0, 0, 0, period_bits, margin_bits);
}

JNIEXPORT void JNICALL Java_buffer29_Trace_flushNative(JNIEnv *env, jclass cls, jboolean active) {
    (void)env;
    (void)cls;
    if (!active_pass) return;
    final_flush = active ? 1 : 0;
    record_event(FINAL_FLUSH, current_pv, NULL, 0, (uint32_t)final_flush, 0, native_writes, 0);
}

/** Delays the selected native PB write, then executes the original kernel I/O. */
ssize_t write(int fd, const void *buffer, size_t length) {
    if (!atomic_load(&enabled) || !active_pass || !current_pv[0] || fd == trace_fd)
        return syscall(SYS_write, fd, buffer, length);
    char link[64], path[PATH_MAX];
    snprintf(link, sizeof(link), "/proc/self/fd/%d", fd);
    ssize_t path_length = readlink(link, path, sizeof(path) - 1);
    if (path_length < 3) return syscall(SYS_write, fd, buffer, length);
    path[path_length] = 0;
    if (strcmp(path + path_length - 3, ".pb")) return syscall(SYS_write, fd, buffer, length);
    copy_name(last_pv, current_pv);
    uint64_t position = native_writes++;
    uint64_t began = monotonic_ns();
    struct stat info;
    off_t offset = lseek(fd, 0, SEEK_CUR);
    int stat_result = fstat(fd, &info);
    record_event(IO_BOUNDARY, current_pv, path, (uint32_t)path_length, (uint32_t)final_flush,
            stat_result ? errno : 0, offset < 0 ? UINT64_MAX : (uint64_t)offset,
            stat_result ? UINT64_MAX : (uint64_t)info.st_size);
    int selected = choose_first ? position == 0
            : !strcmp(current_pv, selected_last) && final_flush;
    if (requested_ns && !injected && selected) {
        struct timespec until = { (time_t)((began + requested_ns) / NANOSECONDS),
                                  (long)((began + requested_ns) % NANOSECONDS) };
        int error;
        do error = clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &until, NULL); while (error == EINTR);
        injected = 1;
        if (phase == EXPECT_LOSS) control_used = 1;
        if (error) atomic_store(&fatal_error, 1);
        record_event(INJECTION, current_pv, path, (uint32_t)path_length, (uint32_t)position,
                error, requested_ns, monotonic_ns() - began);
    }
    ssize_t result = syscall(SYS_write, fd, buffer, length);
    int saved_errno = errno;
    record_event(NATIVE_WRITE, current_pv, path, (uint32_t)path_length, (uint32_t)position,
            result < 0 ? saved_errno : 0, began, result >= 0 ? (uint64_t)result : 0);
    errno = saved_errno;
    return result;
}
