#include <stdio.h>
#include <string.h>
#include <unistd.h>

/* Practice pwn challenge: classic ret2win with no protections. Compiled with
 * -fno-stack-protector -no-pie so the overflow is straightforward and the
 * addresses are static across runs. */

void win(void) {
    printf("flag{stack_smash_and_call_the_neighbors}\n");
}

void vulnerable(void) {
    char buf[64];
    printf("say something: ");
    fflush(stdout);
    fgets(buf, 256, stdin);  /* the bug: size argument doesn't match buf's real size */
    printf("you said: %s\n", buf);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    vulnerable();
    printf("bye\n");
    return 0;
}
