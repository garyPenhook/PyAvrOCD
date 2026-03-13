# UPDI Support Review and Completion Plan

## Purpose

This document summarizes the current UPDI-related state of the PyAvrOCD code base, the gaps that still prevent complete UPDI support, and a concrete implementation plan to finish the work.

The review is based on:

- static inspection of the local `pyavrocd/` code,
- inspection of the local UPDI device database entries,
- inspection of the pinned upstream dependencies declared in `pyproject.toml`,
- comparison with the UPDI support already present in `pymcuprog 3.17.3.45`, and
- execution of the local test suite.

## Baseline

The repository already contains partial UPDI work:

- CLI interface selection includes `updi`.
- `XAvrDebugger` instantiates a UPDI-specific NVM provider.
- `XTinyXAvrTarget` exists as a UPDI-facing target class.
- `XNvmAccessProviderCmsisDapUpdi` exists as a local wrapper.
- There are eight UPDI deviceinfo entries in `pyavrocd/deviceinfo/devices/`.
- There are unit tests that mention UPDI.

The full local test suite passed during this review:

```text
574 passed in 29.14s
```

That green baseline does not mean UPDI is complete. The existing tests mostly validate mocked or partial UPDI plumbing and do not exercise the real runtime control flow used when a GDB client starts a debug session.

## Executive Summary

The most important conclusion is this:

PyAvrOCD does not need a fresh UPDI protocol implementation. The pinned upstream dependency `pymcuprog` already contains working UPDI debug-session and programming primitives for tinyAVR/megaAVR 0/1-style devices. The remaining work is primarily an integration task inside PyAvrOCD's custom debugger, memory-loading, and breakpoint-management layers.

In other words:

- the lower-level UPDI transport and target support already exist upstream,
- this repository has started to expose them,
- but the local abstractions are still shaped around debugWIRE and classic JTAG,
- so the live UPDI code path is incomplete even though the repo already advertises UPDI in several places.

## Current Evidence in the Repository

### What already points to UPDI support

- `pyavrocd/main.py` accepts `updi` as a valid interface.
- `pyavrocd/xavrdebugger.py` creates `XNvmAccessProviderCmsisDapUpdi` when `iface == "updi"`.
- `pyavrocd/deviceinfo/devices/atmega808.py`
- `pyavrocd/deviceinfo/devices/atmega809.py`
- `pyavrocd/deviceinfo/devices/atmega1608.py`
- `pyavrocd/deviceinfo/devices/atmega1609.py`
- `pyavrocd/deviceinfo/devices/atmega3208.py`
- `pyavrocd/deviceinfo/devices/atmega3209.py`
- `pyavrocd/deviceinfo/devices/atmega4808.py`
- `pyavrocd/deviceinfo/devices/atmega4809.py`
- `docs/limitations.md` already discusses UPDI hardware breakpoint count and flash endurance.
- `docs/board-preparation.md`, `docs/connect-to-target.md`, and `docs/adaptation-of-core.md` already mention UPDI targets and probes.

### What still says UPDI is not done

- `README.md` still says "UPDI MCUs will follow next."
- `docs/supported-mcus.md` still says PDI and UPDI "will follow soon."

This mismatch is a useful signal: the code base contains partial implementation, but the project itself does not yet consider the support complete.

## Key Findings

### 1. The UPDI startup path is wired through the wrong debugger contract

#### Evidence

`XAvrDebugger.start_debugging()` in `pyavrocd/xavrdebugger.py` always does this:

- create a housekeeping session,
- call `self.device.avr.setup_debug_session(clkprg=self.clkprg, clkdeb=self.clkdeb, timers_run=self.timers_run)`,
- call `self.device.avr.setup_config(self.device_info)`,
- activate the physical interface,
- attach,
- stop the core,
- optionally manage fuses,
- verify the target,
- reset.

That call shape matches the local debugWIRE and JTAG wrappers, but not the upstream TinyX UPDI API.

The local UPDI target class is `XTinyXAvrTarget` in `pyavrocd/xavr8target.py`. It does not override `setup_debug_session()`. Therefore it inherits the upstream `TinyXAvrTarget.setup_debug_session(interface=..., khz=..., use_hv=...)` signature from `pymcuprog`.

This means the current local call with `clkprg`, `clkdeb`, and `timers_run` is not a valid UPDI setup call.

#### Why it matters

Even before attach, load, breakpoints, or GDB interaction, the UPDI path is structurally incompatible with the local startup sequence.

#### Recommendation

Do not keep one universal startup path that assumes all interfaces share the same lifecycle.

Instead, add an explicit UPDI path in `XAvrDebugger.start_debugging()` or introduce small interface adapters with a common local contract. For UPDI, map PyAvrOCD settings to:

- interface: `AVR8_PHY_INTF_PDI_1W`,
- debug clock / baud: `clkdeb` or a dedicated UPDI frequency setting,
- HV mode: initially `UPDI_HV_NONE`, with optional later exposure.

### 2. `XTinyXAvrTarget` is missing the lifecycle methods that PyAvrOCD expects

#### Evidence

`XTinyXAvrTarget` in `pyavrocd/xavr8target.py` currently adds only:

- register-file helpers,
- SREG helpers,
- stack pointer write,
- hardware breakpoint set/clear.

It does not define the methods that `XAvrDebugger` expects to call generically:

- `attach`,
- `switch_to_progmode`,
- `switch_to_debmode`,
- `reactivate`.

By contrast, the local debugWIRE and JTAG target wrappers do define those methods.

#### Why it matters

Even if startup is fixed, PyAvrOCD later depends on these methods for:

- entering programming mode before flash load,
- returning to debug mode after programming,
- reactivating the session when monitor settings change,
- safe shutdown and reconnect behavior.

#### Recommendation

Add a complete UPDI lifecycle adapter to `XTinyXAvrTarget`, not just register helpers.

The initial implementation should mirror the behavior that `pymcuprog` already expects:

- `attach()`: attach to OCD if needed by the debugger flow,
- `switch_to_progmode()`: detach as necessary, then enter programming mode,
- `switch_to_debmode()`: leave programming mode, reattach, and restore the debug session,
- `reactivate()`: reapply interface configuration and reattach cleanly after option changes.

The exact sequence should be derived from the upstream TinyX behavior, not copied from the JTAG implementation.

### 3. `XNvmAccessProviderCmsisDapUpdi` is still only a stub

#### Evidence

`pyavrocd/xnvmupdi.py` contains only `__init__()` and even starts with the comment:

```python
#Implementation is only a stub:
```

The rest of PyAvrOCD assumes a richer local NVM API. For example:

- `pyavrocd/xavrdebugger.py` calls `self.device.read(...)` with a `prog_mode` argument for flash reads,
- `pyavrocd/memory.py` calls `self.dbg.device.erase_page(...)`,
- `pyavrocd/handler.py` calls `self.dbg.device.erase_chip(...)`,
- `pyavrocd/memory.py` reads and writes EEPROM through `self.dbg.device.read(...)` and `write(...)` with a programming-mode flag.

The upstream `pymcuprog.nvmupdi.NvmAccessProviderCmsisDapUpdi` does provide `read()`, `write()`, and `erase()`, but not the exact local wrapper API already used elsewhere in PyAvrOCD.

#### Why it matters

Without a finished local wrapper, the following features are not reliably available on UPDI:

- flash read in debug mode versus programming mode,
- page erase strategy during wear-minimizing flash load,
- chip erase before load,
- EEPROM read/write through the existing memory abstraction,
- a uniform call surface across interfaces.

#### Recommendation

Implement `XNvmAccessProviderCmsisDapUpdi` so it fully matches the expectations of the rest of the code base.

Minimum methods needed:

- `read(memory_info, offset, numbytes, prog_mode=False)`
- `write(memory_info, offset, data, prog_mode=False)`
- `erase_page(addr, prog_mode)`
- `erase_chip(prog_mode)`

Implementation approach:

- reuse upstream UPDI `read()` and `write()` logic where possible,
- wrap upstream `erase(memory_info, address)` into the page/chip helpers PyAvrOCD already uses,
- keep address handling and alignment behavior consistent with the existing debugWIRE and JTAG wrappers.

### 4. Target verification still assumes debugWIRE-or-JTAG identity semantics

#### Evidence

`XAvrDebugger._verify_target()` in `pyavrocd/xavrdebugger.py` has two paths:

- debugWIRE: derive a signature from the returned `dev_id`,
- everything else: derive a signature using the JTAG-style bit extraction formula.

UPDI currently falls into the "everything else" branch.

That is unsafe because TinyX UPDI devices already have a direct device ID / signature read path upstream. The shape of `activate_physical()` return values should not be assumed to match classic JTAG encoding.

#### Why it matters

Bad identity handling can produce:

- false negatives when connecting to the correct MCU,
- false positives against the wrong MCU,
- brittle behavior across tools and future devices.

#### Recommendation

Make UPDI verification explicit.

Options:

- read the device ID through the upstream UPDI NVM provider and map it to the configured target,
- or read the standard signature bytes directly after activation and compare those.

This should be separate from the JTAG-specific signature derivation logic.

### 5. Memory-area policy for fuses, lockbits, signatures, and user row is currently hard-disabled

#### Evidence

`Memory.mem_area()` in `pyavrocd/memory.py` currently blocks access to:

- fuses,
- lockbits,
- signatures,
- user signature / user row.

There are commented-out branches that explicitly mention `updi`, showing that the code was already considering future enablement.

#### Why it matters

This is not necessarily a blocker for initial UPDI debugging support, but it is a design decision that should be made consciously.

For phase 1, it is reasonable to keep those memory areas blocked if the project wants to avoid:

- accidental fuse modification during a debug session,
- GDB-side writes that could brick a target,
- confusion between "debugging" and "device programming" features.

#### Recommendation

Treat this as a policy decision:

- Phase 1: keep fuse/lock/user-row access blocked in the GDB memory map, but ensure signature comparison still works.
- Phase 2: optionally permit safe read access in programming mode, and possibly guarded write access through explicit monitor commands rather than raw GDB memory writes.

### 6. Existing UPDI tests are too shallow to catch the current gaps

#### Evidence

The current UPDI tests mainly verify:

- object construction,
- getter values,
- a few register helper methods,
- hardware breakpoint helper packet formatting.

They do not verify the real UPDI control flow through:

- `start_debugging()`,
- `switch_to_progmode()`,
- `switch_to_debmode()`,
- `reactivate()`,
- `vFlashErase`,
- `vFlashWrite`,
- `vFlashDone`,
- `X` binary load,
- session stop and detach.

#### Why it matters

This is why the repository can have a green test suite while the live UPDI path is still incomplete.

#### Recommendation

Add UPDI-specific tests at three levels:

1. Target adapter tests
2. NVM wrapper tests
3. End-to-end handler/debugger flow tests

The new tests must exercise the actual methods that were previously missing or incorrectly adapted.

### 7. Documentation is inconsistent with the partial implementation

#### Evidence

The repository already exposes UPDI:

- as a CLI interface,
- in deviceinfo,
- in adaptation docs,
- in board-preparation docs.

But the main project messaging still says UPDI is future work.

#### Why it matters

Users and contributors cannot tell whether they are looking at:

- a hidden experimental feature,
- a half-finished branch,
- or a fully supported feature.

That slows down validation and adoption.

#### Recommendation

Do not update the top-level support claims until the runtime path is actually complete. After the implementation is finished, update:

- `README.md`
- `docs/supported-mcus.md`
- `docs/supported-debuggers.md`
- `docs/limitations.md`

to explicitly describe what is supported, what is experimental, and what still remains out of scope.

## Upstream Capability Already Available

The review of the pinned upstream dependency `pymcuprog 3.17.3.45` shows that the following UPDI pieces already exist upstream:

- `TinyXAvrTarget.setup_prog_session(...)`
- `TinyXAvrTarget.setup_debug_session(...)`
- `TinyXAvrTarget.setup_config(...)`
- `TinyXAvrTarget.activate_physical(...)`
- `NvmAccessProviderCmsisDapUpdi.start(...)`
- `NvmAccessProviderCmsisDapUpdi.read_device_id()`
- `NvmAccessProviderCmsisDapUpdi.erase(...)`
- `NvmAccessProviderCmsisDapUpdi.write(...)`
- `NvmAccessProviderCmsisDapUpdi.read(...)`

That is an important constraint on the design:

PyAvrOCD should reuse those upstream capabilities and wrap them where its local abstractions differ. It should not duplicate the protocol logic unless there is a PyAvrOCD-specific requirement that upstream cannot satisfy.

## Proposed Scope for Phase 1

The most practical first milestone is:

Support the currently listed UPDI megaAVR 0-series style devices already present in the local device database, with a stable debug-session lifecycle and flash loading through the existing GDB server.

Recommended initial target list:

- ATmega808
- ATmega809
- ATmega1608
- ATmega1609
- ATmega3208
- ATmega3209
- ATmega4808
- ATmega4809

Recommended first live-validation device:

- ATmega4809

Reasons:

- it already has local deviceinfo,
- it is referenced by existing tests,
- it is common on boards such as Nano Every and Uno WiFi Rev2,
- it is a good representative of the current UPDI code path.

## Detailed Completion Plan

### Phase 1: Make the live UPDI path work

### 1. Refactor the debugger lifecycle by interface

Files:

- `pyavrocd/xavrdebugger.py`

Tasks:

- stop assuming one `setup_debug_session()` call signature for all interfaces,
- add a dedicated UPDI branch in `start_debugging()`,
- add a dedicated UPDI branch in `_verify_target()`,
- ensure `stop_debugging()` uses a valid UPDI detach/deactivate flow,
- keep debugWIRE and JTAG behavior unchanged.

Expected result:

- UPDI startup no longer fails on method-shape mismatch,
- target validation uses correct UPDI semantics,
- shutdown is symmetrical and explicit.

### 2. Complete the UPDI target adapter

Files:

- `pyavrocd/xavr8target.py`

Tasks:

- add a local UPDI-compatible `setup_debug_session(...)` wrapper,
- add `attach()`,
- add `switch_to_progmode()`,
- add `switch_to_debmode()`,
- add `reactivate()`,
- verify whether `stack_pointer_read()` needs an explicit override or whether the upstream implementation is sufficient,
- verify whether a local `breakpoint_clear()` override is needed for consistency with shutdown.

Expected result:

- `XTinyXAvrTarget` becomes a complete adapter for PyAvrOCD's debugger expectations,
- UPDI joins debugWIRE and JTAG as a first-class interface in the local architecture.

### 3. Complete the UPDI NVM wrapper

Files:

- `pyavrocd/xnvmupdi.py`

Tasks:

- implement `read(..., prog_mode=False)`,
- implement `write(..., prog_mode=False)`,
- implement `erase_page(addr, prog_mode)`,
- implement `erase_chip(prog_mode)`,
- keep `manage` only if it is actually needed for UPDI-specific fuse behavior; otherwise remove or document it.

Expected result:

- UPDI can participate in the existing flash-cache and flash-wear-minimization logic,
- `Memory` and `Handler` no longer need interface-specific special cases just to use UPDI.

### 4. Validate flash-loading behavior

Files:

- `pyavrocd/memory.py`
- `pyavrocd/handler.py`

Tasks:

- verify that page erase strategy for UPDI matches the underlying tool semantics,
- verify that `prog_mode=True` flash reads use the correct memtype through the UPDI wrapper,
- verify that `erase before load` works both for `vFlash*` and `X`,
- verify that EEPROM reads/writes remain correct with the UPDI wrapper.

Expected result:

- `load` works through both standard GDB load styles,
- verify-after-write works,
- EEPROM access behaves consistently with the existing abstractions.

### 5. Validate breakpoint and execution control

Files:

- `pyavrocd/xavr8target.py`
- `pyavrocd/breakexec.py`
- `pyavrocd/hardwarebp.py`

Tasks:

- confirm that two hardware breakpoints are available and exposed correctly,
- verify that software breakpoints still work on UPDI flash targets,
- validate continue, single-step, range-step, and reset interactions,
- confirm that the temporary hardware-breakpoint slot logic behaves correctly with only two slots.

Expected result:

- UPDI execution control works with the same GDB command set already used for debugWIRE and JTAG,
- breakpoint allocation does not regress due to the lower hardware-breakpoint count.

### Phase 2: Improve robustness and extend support

### 6. Expose high-voltage UPDI options intentionally

Files:

- `pyavrocd/main.py`
- `pyavrocd/xavrdebugger.py`
- `pyavrocd/xnvmupdi.py`
- documentation

Tasks:

- decide whether HV UPDI should be a CLI option, a monitor command, or left internal for now,
- expose only the modes that can be described and tested clearly,
- document tool limitations by probe type.

Expected result:

- recovery of shared-UPDI or misconfigured UPDI pins becomes possible where the hardware supports it,
- users understand the risk and required wiring.

### 7. Revisit memory-area policy

Files:

- `pyavrocd/memory.py`
- documentation

Tasks:

- decide whether signatures should be readable through GDB memory access,
- decide whether user row read/write should be available in programming mode,
- keep fuse and lockbit writes protected unless there is a strong use case.

Expected result:

- UPDI devices expose the right level of programmability without making debugging dangerous.

### 8. Broaden device coverage

Files:

- `pyavrocd/deviceinfo/devices/`
- harvesting scripts if needed

Tasks:

- validate the current eight devices live,
- then expand to additional UPDI-capable families only after confirming that the current abstractions remain correct.

Expected result:

- support grows from a validated base instead of widening the matrix too early.

## Test Plan

### Unit Tests to Add

#### `tests/test_xavrdebugger.py`

Add UPDI tests for:

- successful `start_debugging()` on a UPDI target,
- correct UPDI-specific `setup_debug_session()` call shape,
- correct attach / stop / reset flow,
- correct target verification path,
- correct `switch_to_progmode()` and `switch_to_debmode()` dispatch.

#### `tests/test_xnvmupdi.py`

Add tests for:

- flash `read()` in debug mode and programming mode,
- flash `write()` alignment and chunking,
- EEPROM read/write path,
- `erase_page()`,
- `erase_chip()`,
- error handling on unsupported memory types.

#### `tests/test_xavr8target_updi.py`

Add tests for:

- `setup_debug_session()` wrapper,
- `attach()`,
- `switch_to_progmode()`,
- `switch_to_debmode()`,
- `reactivate()`,
- any additional stack-pointer or breakpoint-clear behavior implemented locally.

#### Handler / memory tests

Relevant files:

- `tests/test_memory.py`
- `tests/test_gdbhandler.py` if present in the local branch
- any existing handler tests that validate `vFlashErase`, `vFlashWrite`, `vFlashDone`, and `X`

Add tests for:

- UPDI flash loading through `vFlash*`,
- UPDI flash loading through binary `X`,
- erase-before-load behavior,
- verify-after-load behavior,
- EEPROM memory access through the GDB handler.

## Live / Integration Validation

Recommended first hardware matrix:

- MCU: ATmega4809
- Probes: one EDBG-derived probe and one non-EDBG Microchip probe if available

Recommended first live scenarios:

1. start session from GDB `qSupported`
2. read registers
3. write registers
4. load flash with `vFlash*`
5. load flash with binary `X`
6. read and write EEPROM
7. set software breakpoint
8. set hardware breakpoint
9. continue
10. single-step
11. reset
12. detach
13. reconnect

Only after those pass should the README claim full UPDI support.

## Suggested Order of Work

The safest order is:

1. complete `XTinyXAvrTarget`
2. complete `XNvmAccessProviderCmsisDapUpdi`
3. split or branch UPDI logic in `XAvrDebugger`
4. add unit tests for the new lifecycle and NVM wrapper
5. validate `Memory` and `Handler` flash-load behavior
6. run live hardware validation
7. update top-level docs and support claims

This order reduces the chance of changing documentation before the runtime path is actually usable.

## Risks and Constraints

#### Flash endurance

UPDI devices typically have lower guaranteed flash endurance than classic AVRs. PyAvrOCD's existing flash-wear-aware behavior is therefore especially important and should not be bypassed for the sake of a quick bring-up.

#### Tool differences

High-voltage UPDI activation and some reattach sequences may vary by probe capability. The implementation should not assume all EDBG-derived tools support the same UPDI extras.

#### Mocked tests can hide integration defects

The existing suite shows that interface wiring issues can be hidden behind mocks. Any completion effort must include at least one live validation target.

## Completion Criteria

UPDI support should be considered complete for phase 1 when all of the following are true:

- a UPDI target can start a session from a normal GDB connection,
- flash load works through both `vFlash*` and binary `X`,
- EEPROM access works,
- register access works,
- continue / step / reset / detach work,
- both software and hardware breakpoints work within the expected limits,
- the unit suite covers the live control-flow branches that were previously untested,
- the top-level documentation no longer describes UPDI as future work.

## Final Recommendation

Treat the remaining UPDI work as an adapter-completion and integration-hardening task, not as a new protocol project.

The fastest correct route is:

- reuse the UPDI functionality already present in `pymcuprog`,
- finish the local `XTinyXAvrTarget` and `XNvmAccessProviderCmsisDapUpdi` wrappers,
- make `XAvrDebugger` explicitly interface-aware instead of assuming debugWIRE/JTAG semantics,
- then add the tests that should have existed before the feature was exposed in the CLI.

That approach keeps the change set bounded, preserves PyAvrOCD's existing abstractions, and gives the project a clear point at which the README and support matrix can be updated without overstating the current state.
