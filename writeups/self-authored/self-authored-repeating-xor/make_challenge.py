#!/usr/bin/env python3
"""Generates ciphertext.bin: a plaintext repeating-key XOR'd with a secret key.
This is the challenge generator, not part of the solve — kept here so the
challenge is reproducible and clearly self-authored.

The plaintext is long enough (roughly 1.5 KB) for the Hamming-distance key
length guess to have enough samples to be reliable; a couple hundred bytes
is too short for that statistic to separate the real key length from noise.
"""

PLAINTEXT = b"""the flag is flag{vigenere_never_really_left_us}. repeating key xor is just
vigenere over bytes instead of letters, and it falls to the exact same attack
that breaks vigenere ciphers: find the key length first, then solve each
column as its own independent single byte xor.

the key length guess works because xor-ing two blocks of ciphertext that are
both aligned to the start of a key period cancels the key out entirely,
leaving you with plaintext xor plaintext. two blocks of real english text
have a lower hamming distance on average than two blocks of random bytes,
so the correct key length shows up as a dip in the average normalized
hamming distance across candidate lengths, while wrong lengths look closer
to random.

once the key length is known, split the ciphertext into that many
interleaved columns. every byte in a given column was xored with the exact
same key byte, which turns each column into an ordinary single byte xor
problem, solvable by brute forcing all two hundred fifty six candidate keys
and scoring the result against english letter frequency, exactly the same
scoring heuristic a single byte xor bruteforcer already uses.

put the recovered key bytes back in order and the whole ciphertext falls to
one repeating xor pass, no guessing involved once the statistics point at
the right key length.
"""
KEY = b"shadow"

if __name__ == "__main__":
    ciphertext = bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(PLAINTEXT))
    with open("ciphertext.bin", "wb") as f:
        f.write(ciphertext)
    print(f"wrote ciphertext.bin ({len(ciphertext)} bytes), key length {len(KEY)}")
