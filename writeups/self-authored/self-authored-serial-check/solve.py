#!/usr/bin/env python3
"""Recover the serial for crackme.exe by inverting the per-byte check:

    scrambled[i] = (input[i] + key[i]) ^ key[(i+1) % len(key)]

Inverting: input[i] = (scrambled[i] ^ key[(i+1) % len(key)]) - key[i]
"""

key = [0x13, 0x37, 0x42, 0x99, 0x01, 0x7a, 0x2c, 0xf0]
target = [0x61, 0xcb, 0xef, 0xdd, 0x36, 0xeb, 0xaf, 0x02]

serial = []
for i, t in enumerate(target):
    unxored = t ^ key[(i + 1) % len(key)]
    ch = (unxored - key[i]) & 0xff
    serial.append(chr(ch))

print("".join(serial))
