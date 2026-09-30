#include <stdio.h>
#include <string.h>

/* Practice crackme: type the right serial and it prints the flag.
 * The check is deliberately simple (obfuscated addition, not real crypto) —
 * this exists to have something concrete to reverse in the writeup, not to
 * be a hard challenge. */

static void check(const char *input) {
    unsigned char key[] = { 0x13, 0x37, 0x42, 0x99, 0x01, 0x7a, 0x2c, 0xf0 };
    unsigned char target[] = { 0x61, 0xcb, 0xef, 0xdd, 0x36, 0xeb, 0xaf, 0x02 };
    size_t len = strlen(input);

    if (len != sizeof(key)) {
        printf("nope\n");
        return;
    }

    for (size_t i = 0; i < len; i++) {
        unsigned char scrambled = (unsigned char)(input[i] + key[i]) ^ key[(i + 1) % sizeof(key)];
        if (scrambled != target[i]) {
            printf("nope\n");
            return;
        }
    }

    printf("flag{that_was_addition_and_xor_all_along}\n");
}

int main(int argc, char **argv) {
    if (argc != 2) {
        printf("usage: %s <serial>\n", argv[0]);
        return 1;
    }
    check(argv[1]);
    return 0;
}
