# UPDI Phase 1 Change Note

This note records the UPDI-related implementation, testing, device-database work, and later hardware validation added in this workspace session.

The code completion and drafting work in this session was aided by ChatGPT operating in the local workspace.

This note does not claim sole authorship of the surrounding PyAvrOCD code base, the upstream `pymcuprog` UPDI implementation, or the broader project design.

## Scope of changes in this session

The following additions and changes were made to the project as part of this first UPDI implementation pass.

### Runtime code changes

- completed the local UPDI target adapter in `pyavrocd/xavr8target.py`
- completed the local UPDI NVM wrapper in `pyavrocd/xnvmupdi.py`
- adjusted UPDI target verification in `pyavrocd/xavrdebugger.py`
- corrected flash memory-map reporting in `pyavrocd/memory.py` so GDB loads use the logical flash address space instead of the raw UPDI NVM base address

### Test additions and expansions

- expanded UPDI target adapter tests in `tests/test_xavr8target_updi.py`
- expanded UPDI NVM wrapper tests in `tests/test_xnvmupdi.py`
- added UPDI verification coverage in `tests/test_xavrdebugger.py`
- added UPDI memory-path coverage in `tests/test_memory.py`
- added UPDI handler and flash-load coverage in `tests/test_gdbhandler.py`
- added regression coverage for the UPDI raw-signature read path and for flash memory-map reporting

### Device database additions

- added tinyAVR UPDI device-info modules harvested from the local `ATtiny_DFP 3.3.272` pack
- regenerated `pyavrocd/deviceinfo/devices/alldevices.py` so the CLI and signature lookup paths recognize the new parts

### Documentation additions

- added `docs/updi-support-plan.md`
- added this change record in `docs/updi-phase1-change-note.md`

## Detailed summary of what was implemented

### 1. UPDI target lifecycle support

The local TinyX wrapper in `pyavrocd/xavr8target.py` was extended so the UPDI path matches the lifecycle expected by PyAvrOCD.

The implementation added:

- a PyAvrOCD-compatible `setup_debug_session(...)` shim for the TinyX target
- `attach()`
- `switch_to_progmode()`
- `switch_to_debmode()`
- `reactivate()`

This was done so the debugger can use the UPDI target through the same higher-level flow already used for other interfaces.

### 2. UPDI NVM access completion

The local UPDI NVM wrapper in `pyavrocd/xnvmupdi.py` was expanded from a stub into a working adapter that matches the APIs already used in the project.

The implementation added:

- `read(memory_info, offset, numbytes, prog_mode=False)`
- `write(memory_info, offset, data, prog_mode=False)`
- `erase_page(addr, prog_mode)`
- `erase_chip(prog_mode)`

This completed the local interface needed by the debugger, handler, and memory layers for UPDI programming-mode operations.

### 3. UPDI target verification fix

`pyavrocd/xavrdebugger.py` was changed so UPDI targets are verified by reading signature bytes directly rather than reusing the JTAG-style `dev_id` interpretation path.

This reduced the risk of misidentifying TinyX UPDI devices during session startup.

### 4. Memory-path and flash-load coverage

Additional coverage was added for the live programming path used by the GDB server.

The added tests cover:

- UPDI flash erase and flash completion handling
- UPDI binary flash writes through the `X` packet path
- page erase behavior during flash programming
- EEPROM read and write behavior with programming-mode forwarding

This coverage was added primarily in `tests/test_memory.py` and `tests/test_gdbhandler.py`.

### 5. Session startup and shutdown coverage

Additional handler tests were added around the UPDI startup path so the GDB-side session flow is exercised more directly.

The added tests cover:

- UPDI `qSupported` startup with `warmstart=False`
- continued debugWIRE behavior with `warmstart=True`
- cleanup behavior when UPDI startup fails
- the normal path that marks the debugger active after a successful UPDI start

### 6. TinyAVR device-pack expansion

The local device database was expanded to include missing tinyAVR UPDI devices already present in the repository ATDF mirror under `extras/atdf/tiny-3.3.272`.

The following device groups were added:

- `ATtiny202`, `ATtiny204`, `ATtiny212`, `ATtiny214`
- `ATtiny1604`, `ATtiny1606`, `ATtiny1607`
- `ATtiny1614`, `ATtiny1616`, `ATtiny1617`
- `ATtiny1624`, `ATtiny1626`, `ATtiny1627`
- `ATtiny3216`, `ATtiny3217`
- `ATtiny3224`, `ATtiny3226`, `ATtiny3227`
- `ATtiny402`, `ATtiny404`, `ATtiny406`
- `ATtiny412`, `ATtiny414`, `ATtiny416`, `ATtiny417`
- `ATtiny424`, `ATtiny426`, `ATtiny427`
- `ATtiny804`, `ATtiny806`, `ATtiny807`
- `ATtiny814`, `ATtiny816`, `ATtiny817`
- `ATtiny824`, `ATtiny826`, `ATtiny827`

This work added harvested `DEVICE_INFO` modules under `pyavrocd/deviceinfo/devices/` and refreshed the aggregate `alldevices.py` index used by the CLI and device lookup logic.

`ATtiny40` was reviewed but not added as part of this UPDI work because its pack metadata reports interface `TPI`, not `UPDI`.

### 7. Device registration coverage

A focused device-info test was added and expanded in `tests/test_deviceinfo_tiny_updi.py`.

That test now checks:

- registration of the newly added tinyAVR UPDI parts in `dev_id`, `dev_name`, and `dev_iface`
- pack-derived memory layout expectations across the `20x`, `40x`, `80x`, `160x`, `161x`, `162x`, `321x`, and `322x` families
- continued visibility of the new parts through the CLI-oriented device tables

### 8. Hardware smoke-test validation

Additional follow-up work was done after the initial UPDI implementation pass to validate the live execution path on real hardware.

The hardware used for this smoke test was:

- `ATtiny3217` target firmware from the local `test_nano_C` project
- Curiosity Nano mounted on a Curiosity Nano Explorer
- onboard `nEDBG CMSIS-DAP` debugger exposed by the Nano

The first real smoke test exposed a runtime bug: UPDI startup reached the target, but target verification read the wrong signature value because the implementation was using the wrong access path for TinyX UPDI devices.

That defect was corrected by changing the UPDI signature read logic in `pyavrocd/xavrdebugger.py` to read the raw signature bytes from the TinyX signature row in programming mode.

The same smoke-test work also exposed a second live issue: normal GDB `load` failed when PyAvrOCD advertised flash in the memory map using the raw flash NVM base address instead of the ELF-visible flash start address.

That defect was corrected in `pyavrocd/memory.py` by using the flash `hexfile_address` for the GDB memory map while preserving the raw address for programming operations.

After those fixes, a real `avr-gdb` smoke test completed successfully through the normal remote-debug flow:

- connect
- verify `ATtiny3217` signature `0x1E9522`
- `monitor reset`
- `load`
- set breakpoint at `main`
- `continue`
- stop at `main`
- read registers
- detach

### 9. Project documentation additions

Two documentation files were added during this work:

- `docs/updi-support-plan.md` records the original review, findings, implementation gaps, and recommended next steps for full UPDI support
- `docs/updi-phase1-change-note.md` records the specific changes made in this implementation pass

## Files changed in this implementation pass

- `pyavrocd/xavr8target.py`
- `pyavrocd/xnvmupdi.py`
- `pyavrocd/xavrdebugger.py`
- `pyavrocd/memory.py`
- `pyavrocd/deviceinfo/devices/alldevices.py`
- `pyavrocd/deviceinfo/devices/attiny202.py`
- `pyavrocd/deviceinfo/devices/attiny204.py`
- `pyavrocd/deviceinfo/devices/attiny212.py`
- `pyavrocd/deviceinfo/devices/attiny214.py`
- `pyavrocd/deviceinfo/devices/attiny402.py`
- `pyavrocd/deviceinfo/devices/attiny404.py`
- `pyavrocd/deviceinfo/devices/attiny406.py`
- `pyavrocd/deviceinfo/devices/attiny412.py`
- `pyavrocd/deviceinfo/devices/attiny414.py`
- `pyavrocd/deviceinfo/devices/attiny416.py`
- `pyavrocd/deviceinfo/devices/attiny417.py`
- `pyavrocd/deviceinfo/devices/attiny424.py`
- `pyavrocd/deviceinfo/devices/attiny426.py`
- `pyavrocd/deviceinfo/devices/attiny427.py`
- `pyavrocd/deviceinfo/devices/attiny804.py`
- `pyavrocd/deviceinfo/devices/attiny806.py`
- `pyavrocd/deviceinfo/devices/attiny807.py`
- `pyavrocd/deviceinfo/devices/attiny814.py`
- `pyavrocd/deviceinfo/devices/attiny816.py`
- `pyavrocd/deviceinfo/devices/attiny817.py`
- `pyavrocd/deviceinfo/devices/attiny824.py`
- `pyavrocd/deviceinfo/devices/attiny826.py`
- `pyavrocd/deviceinfo/devices/attiny827.py`
- `pyavrocd/deviceinfo/devices/attiny1604.py`
- `pyavrocd/deviceinfo/devices/attiny1606.py`
- `pyavrocd/deviceinfo/devices/attiny1607.py`
- `pyavrocd/deviceinfo/devices/attiny1614.py`
- `pyavrocd/deviceinfo/devices/attiny1616.py`
- `pyavrocd/deviceinfo/devices/attiny1617.py`
- `pyavrocd/deviceinfo/devices/attiny1624.py`
- `pyavrocd/deviceinfo/devices/attiny1626.py`
- `pyavrocd/deviceinfo/devices/attiny1627.py`
- `pyavrocd/deviceinfo/devices/attiny3216.py`
- `pyavrocd/deviceinfo/devices/attiny3217.py`
- `pyavrocd/deviceinfo/devices/attiny3224.py`
- `pyavrocd/deviceinfo/devices/attiny3226.py`
- `pyavrocd/deviceinfo/devices/attiny3227.py`
- `tests/test_xavr8target_updi.py`
- `tests/test_xnvmupdi.py`
- `tests/test_xavrdebugger.py`
- `tests/test_memory.py`
- `tests/test_gdbhandler.py`
- `tests/test_deviceinfo_tiny_updi.py`
- `docs/updi-support-plan.md`
- `docs/updi-phase1-change-note.md`

## Validation

The work was validated incrementally with focused UPDI-related test runs and with full-suite runs during the session.

The recorded verification results for this implementation pass include:

```text
593 passed in 30.14s
46 passed in 0.16s
197 passed in 15.49s
243 passed in 17.81s
```

In addition to the automated test runs above, the later smoke-test validation on real hardware succeeded with the local `ATtiny3217` firmware project under `avr-gdb`.

## Intent

This note is meant to document the specific project additions and changes made in this workspace session. It should be read together with `docs/updi-support-plan.md`, which contains the broader review, findings, and remaining work still needed for more complete UPDI support.
