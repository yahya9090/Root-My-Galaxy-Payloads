# Samsung Galaxy Z Flip 6 (SM-F741B) GKI 6.1.162 Port & Validation Record

## Device Specification
- **Model:** Samsung Galaxy Z Flip 6 (`SM-F741B`, board `b6q`)
- **Platform:** Qualcomm Snapdragon 8 Gen 3 (`pineapple`)
- **Firmware:** `F741BXXU4EZIH` (One UI 9.0 Preview)
- **Kernel:** `6.1.162-android14-11-34343818-abF741BXXU4EZIH` (aarch64)
- **Knox Warranty Bit:** `0x0` (Enforcing)

## Architecture & Compatibility
1. **Snapdragon 8 Gen 3 (Pineapple) GKI Identity:**
   - Both `SM-S928B` (S24 Ultra) and `SM-F741B` share identical GKI build hash `34343818` (vermagic `6.1.162-android14-11-34343818-abS928BXXU6EZIF`).
   - The Samsung KDP/DEFEX late-loaded driver `ksud-e3q-S928BXXU6EZIF-kdp` is 100% binary-interchangeable.

2. **KernelSU Manager UAPI Alignment:**
   - The late-loaded LKM implements KernelSU UAPI v2 (`versionCode 32601`).
   - Pinned Manager: `KernelSU_v3.3.0_32601-release.apk` (UAPI v2).
   - Higher versions (v3.3.1 / 32680, UAPI v5) trigger `Error: UAPI version mismatch: kernel=2, ksud=5` during module flashing.

3. **DirtyFrag Stage 2 Resolution (Root Without Exploit):**
   - The secondary loader in Root My Galaxy Next (`dev.rushiranpise.rmgnext`) failed at Step 3 (`patch_ko`):
     `patch #2 ret -1`
   - Cause: `libexp.so` at instruction `0x1712c` loaded literal string `[vendorfile]` instead of `/vendor/lib64/libstagefrighthw.so`.
   - Fix: Instruction patched to `add x0, x0, #9` via `tools/patch_dirtyfrag_stage2.py`, successfully targeting `/vendor/lib64/libstagefrighthw.so` (31,928 bytes).
