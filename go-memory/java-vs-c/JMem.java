public class JMem {
    public static void main(String[] args) throws InterruptedException {
        long total = Runtime.getRuntime().totalMemory();
        long free  = Runtime.getRuntime().freeMemory();
        System.out.printf("Used JVM heap = %.2f MB%n", (total - free) / 1024.0 / 1024.0);

        // Keep the process alive indefinitely:
        System.out.println("JVM paused. PID=" + ProcessHandle.current().pid() +
                           " — press Ctrl+C to exit.");
        Thread.sleep(Long.MAX_VALUE);
    }
}
