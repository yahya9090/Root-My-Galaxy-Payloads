#!/usr/bin/env python3
"""
patch_dirtyfrag_stage2.py

Patches lib/arm64-v8a/libexp.so inside Root My Galaxy Next stage2.apk.
Fixes the DirtyFrag page-cache splice bug on Samsung Galaxy Z Flip 6 / S24 Ultra (Pineapple 6.1.162):
At instruction 0x1712c, patches 'add x0, x0, #0x12c' ([vendorfile])
to 'add x0, x0, #9' (/vendor/lib64/libstagefrighthw.so), preventing ENOENT (patch #2 ret -1).
"""

import sys
import zipfile
import io

def patch_libexp(data: bytearray) -> bytearray:
    # Target virtual address: 0x1712c, .text file offset: 0x1312c
    target_offset = 0x1712c - 0x4000
    orig_insn = bytes.fromhex("00b00491")  # add x0, x0, #0x12c ([vendorfile])
    fixed_insn = bytes.fromhex("00240091") # add x0, x0, #9 (/vendor/lib64/libstagefrighthw.so)

    if data[target_offset:target_offset+4] != orig_insn:
        # Check if already patched
        if data[target_offset:target_offset+4] == fixed_insn:
            print("[*] libexp.so already patched at 0x1712c.")
            return data
        raise ValueError(f"Unexpected bytes at 0x1712c: {data[target_offset:target_offset+4].hex()}")

    data[target_offset:target_offset+4] = fixed_insn
    print("[+] Patched 0x1712c -> add x0, x0, #9 (pointing to /vendor/lib64/libstagefrighthw.so)")
    return data

def patch_stage2_apk(in_apk_path: str, out_apk_path: str):
    with open(in_apk_path, "rb") as f:
        in_zip = zipfile.ZipFile(f)
        out_buf = io.BytesIO()
        out_zip = zipfile.ZipFile(out_buf, "w", compression=zipfile.ZIP_DEFLATED)

        for item in in_zip.infolist():
            content = in_zip.read(item.filename)
            if item.filename == "lib/arm64-v8a/libexp.so":
                content = bytes(patch_libexp(bytearray(content)))
            out_zip.writestr(item, content)

        in_zip.close()
        out_zip.close()

    with open(out_apk_path, "wb") as f:
        f.write(out_buf.getvalue())
    print(f"[+] Output written to {out_apk_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: patch_dirtyfrag_stage2.py <in_stage2.apk> <out_stage2.apk>")
        sys.exit(1)
    patch_stage2_apk(sys.argv[1], sys.argv[2])
