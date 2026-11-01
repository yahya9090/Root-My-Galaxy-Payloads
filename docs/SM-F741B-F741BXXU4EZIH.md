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

4. **Pixel Transformation Suite (Zero Full Reboots):**
   - **LSPosed Bridge (`dev.pixel.oneui.bridge`):**
     - `QSTileViewImpl`: Enforces Material 3 Expressive 80dp pill geometry (28dp radius, 16dp horizontal padding).
     - `ScrimController` & `SecQpBlurController`: Suppresses Samsung OEM tint curves and maps shade background to `@android:color/system_neutral1_900` (`#1B1B1F`) and active tiles to `@android:color/system_accent1_100` (`#E1E0FF`).
     - `OverviewProxyService`: Forces `config_recentsComponentName` to return `app.lawnchair/com.android.quickstep.TouchInteractionService`.
     - `system_server`: Injects runtime privileged permissions (`STATUS_BAR_SERVICE`, `CONTROL_REMOTE_APP_TRANSITION_ANIMATIONS`, `MANAGE_ACTIVITY_TASKS`) and sets `PRIVATE_FLAG_PRIVILEGED` on non-system launchers without partition writes.
     - `Cover Screen Continuity`: Detects display ID != 0 (Flex Window subscreen) and delegates launcher handling to `com.sec.android.app.launcher` while maintaining Lawnchair on the main foldable display.
   - **Hot-Reload:**
     - All modules apply dynamically via `su -c "pkill -f com.android.systemui"`. Zero full kernel reboots required.
