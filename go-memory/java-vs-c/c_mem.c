#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/resource.h>

int main(void) {
    pid_t pid = getpid();
    printf("PID = %d\n", pid);

    struct rusage u;
    if (getrusage(RUSAGE_SELF, &u) != 0) {
        perror("getrusage");
        return 1;
    }
    printf("Max RSS = %ld KB\n", u.ru_maxrss);

    // Hold the process so you can inspect it externally:
    printf("Sleeping indefinitely. Attach with `pmap -x %d` or `ps -p %d`...\n", pid, pid);
    fflush(stdout);

    // sleep forever (until you kill it)
    while (1) {
        sleep(60);
    }

    return 0;
}
