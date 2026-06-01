# Architecture

PyAvrOCD is a single Python package, `pyavrocd`, that sits between GDB and a Microchip debug probe. This page documents how the code is organized and how a debug session flows through it.

## High-level data flow

```
            ┌──────────────────────────────────────────────────────────┐
   GDB ─────▶  RspServer        accept TCP connection on port (def 2000) │
 (RSP/TCP)  │     │                                                      │
            │     ▼                                                      │
            │  GdbHandler      parse RSP packets, dispatch commands      │
            │     │                                                      │
            │     ├─▶ MonitorCommand     handle `monitor …` commands     │
            │     ├─▶ BreakAndExec       breakpoints, step, continue     │
            │     ├─▶ Memory             flash / SRAM / EEPROM access    │
            │     │                                                      │
            │     ▼                                                      │
            │  XAvrDebugger    high-level target abstraction             │
            │     │                                                      │
            │     ▼                                                      │
            │  XTinyXAvrTarget / XTinyAvrTarget / XMegaAvrJtagTarget /   │
            │  XXmegaAvrTarget        (per-architecture target classes)  │
            │     │                                                      │
            │     ▼                                                      │
            │  XNvm…Debugwire / …Updi / …MegaAvrJtag   NVM access layer  │
            └─────┼──────────────────────────────────────────────────────┘
                  ▼
            pyedbglib / pymcuprog  ──USB/CMSIS-DAP──▶  Debug probe ─▶ AVR
```

PyAvrOCD builds on Microchip's own libraries — **`pymcuprog`** (device programming/NVM backends) and **`pyedbglib`** (CMSIS-DAP / EDBG transport) — and extends their classes (the `X…` prefix throughout the codebase means "extended").

## Module map

The package lives in `pyavrocd/`. Core modules:

| Module | Key class(es) | Responsibility |
|--------|---------------|----------------|
| `main.py` | — | CLI entry point: argument parsing, tool discovery, USB connection, server startup. Exposes the `pyavrocd` console script via `main()`. |
| `server.py` | `RspServer` | TCP socket server speaking the GDB Remote Serial Protocol; the session loop. |
| `handler.py` | `GdbHandler` | Parses RSP packets and dispatches them to the right subsystem. |
| `monitor.py` | `MonitorCommand` | Implements all `monitor …` commands and holds session state (caching, breakpoint policy, timers, etc.). |
| `breakexec.py` | `BreakAndExec` | Breakpoint management and execution control (continue, single-step, range-step), including interrupt-safe stepping. |
| `hardwarebp.py` | `HardwareBP` | Allocation/bookkeeping of the limited hardware breakpoint resources. |
| `memory.py` | `Memory` | Read/write of flash, SRAM, and EEPROM; flash caching to reduce wear. |
| `instructions.py` | — | AVR opcode helpers used by the stepping/breakpoint logic. |
| `errors.py` | `FatalError`, `EndOfSession` | Exception types that control session termination. |
| `dwlink.py` | `SerialToNet`, `DetachException` | Pass-through bridge to the serial-based `dw-link` probe. |
| `livetests.py` | `LiveTests` | On-target self-tests reachable via a `monitor` command. |

## Target / NVM abstraction layers

These classes subclass `pymcuprog` types to adapt them to GDB-server use:

| Module | Class | Wraps |
|--------|-------|-------|
| `xavrdebugger.py` | `XAvrDebugger` | `pymcuprog` `AvrDebugger` — the central target handle; also hosts `sram_masked_read/write`. |
| `xavr8target.py` | `XTinyXAvrTarget` | tinyAVR/megaAVR-0/AVR-Dx (UPDI) target |
| | `XTinyAvrTarget` | classic debugWIRE target |
| | `XMegaAvrJtagTarget` | megaAVR JTAG target |
| | `XXmegaAvrTarget` | Xmega (PDI) target |
| `xnvmdebugwire.py` | `XNvmAccessProviderCmsisDapDebugwire` | debugWIRE NVM access |
| `xnvmupdi.py` | `XNvmAccessProviderCmsisDapUpdi` | UPDI NVM access |
| `xnvmmegaavrjtag.py` | `XNvmAccessProviderCmsisDapMegaAvrJtag` | megaAVR JTAG NVM access |

## Device information

`pyavrocd/deviceinfo/` holds per-device data and the tooling that generates it:

- `devices/` — ~280 generated Python modules, one per MCU (memory layout, signature, fuses, I/O registers), plus `alldevices.py` which aggregates `dev_id` and `dev_iface` lookup tables used by `main.py`.
- `harvest.py` — collects device parameters into the device modules.
- `addsvd.py` — reads an SVD file and embeds it as a Python data structure into the matching device module (run after `harvest.py`); SVD sources live in the top-level `svd/` directory.
- `collect.py` — supporting collection logic.

## Startup sequence (in `main.py`)

1. `options()` parses the command line (and an optional `pyavrocd.options` file).
2. `process_arguments()` validates the device, resolves the debug interface, and expands fuse-management flags.
3. If `-s simavr` was given, `handle_simavr()` launches the simulator and exits.
4. The ELF file (if supplied) is checked for the unsupported `-mrelax` optimization.
5. Connected EDBG probes are discovered over USB and one is selected (`-t`/`-u` disambiguate).
6. An `XAvrDebugger` is created for the device/interface, wrapped in an `RspServer`.
7. `server.serve()` runs the RSP session loop until GDB disconnects or a fatal error occurs.
