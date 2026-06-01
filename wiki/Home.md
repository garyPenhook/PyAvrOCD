# PyAvrOCD Wiki

**PyAvrOCD** is a cross-platform GDB server for 8-bit AVR microcontrollers. It lets you debug programs running on real AVR MCUs (and the `simavr` simulator) using the standard [GNU Debugger (GDB)](https://www.sourceware.org/gdb/), and it is designed to be *the missing AVR debugging solution* for the **Arduino IDE 2** and **PlatformIO**.

It talks to Microchip debug probes such as the affordable [MPLAB Snap](https://www.microchip.com/en-us/development-tool/pg164100), Atmel-ICE, PICkit 4, Power Debugger, and the EDBG probes on Curiosity Nano / Xplained boards. It also provides a pass-through service for the UNO-based [dw-link](https://github.com/felias-fogg/dw-link) probe and the [simavr](https://github.com/buserror/simavr) simulator.

> This wiki documents the **`garyPenhook/PyAvrOCD`** fork. The upstream project lives at [felias-fogg/PyAvrOCD](https://github.com/felias-fogg/PyAvrOCD) and the official docs are at [pyavrocd.io](https://pyavrocd.io).

## Quick links

| Page | What's inside |
|------|---------------|
| [[Project Status]] | Current version, fork state, CI, and roadmap |
| [[Architecture]] | How the software is structured (modules, classes, data flow) |
| [[Installation]] | How to install and run the server |
| [[Usage]] | Command-line options and `monitor` commands |
| [[Supported Hardware]] | Supported MCUs, interfaces, and debug probes |
| [[Development]] | Building, testing, and contributing |

## What it does, in one diagram

```
   GDB  ──TCP/RSP──▶  PyAvrOCD  ──USB/CMSIS-DAP──▶  Debug probe  ──▶  AVR target
 (avr-gdb)          (this server)                  (Snap, ICE…)      (ATmega/ATtiny/AVR-Dx…)
```

GDB connects to PyAvrOCD over a TCP socket (default port **2000**) speaking the GDB Remote Serial Protocol (RSP). PyAvrOCD translates RSP requests into low-level operations on the chosen debug interface — **debugWIRE**, **JTAG**, **PDI**, or **UPDI** — and drives the AVR target through a Microchip debug probe.

## Key features

- **Cross-platform** — Linux, macOS, and Windows.
- **Four debug interfaces** — debugWIRE, JTAG (megaAVR), PDI, UPDI.
- **~280 supported MCUs** — classic ATmega/ATtiny through the modern tinyAVR, megaAVR-0, and AVR Dx/Ex families.
- **Flash-wear friendly** — caching and read-before-write minimize flash erase/write cycles.
- **Interrupt-safe single-stepping** — single steps are protected against interrupts.
- **Rich `monitor` commands** — including the new `monitor ioregister` for inspecting/changing I/O registers and bitfields live.
