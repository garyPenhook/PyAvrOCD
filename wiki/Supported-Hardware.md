# Supported Hardware

## Debug interfaces

PyAvrOCD speaks four on-chip debug interfaces. The interface is auto-detected from the chosen device, or can be forced with `-i`:

| Interface | Typical targets |
|-----------|-----------------|
| **debugWIRE** | Classic ATtiny and smaller ATmega parts (single-wire over RESET). |
| **JTAG** | Larger megaAVR parts with a JTAG port. |
| **UPDI** | Modern tinyAVR-0/1/2, megaAVR-0, AVR Dx/Ex families. |
| **PDI** | Xmega parts (limited; see roadmap). |

List interfaces at runtime with `pyavrocd -i ?`.

## Debug probes (tools)

Selected with `-t`; query the list with `pyavrocd -t ?`:

| Tool id | Probe |
|---------|-------|
| `snap` | MPLAB Snap (low-cost) |
| `atmelice` | Atmel-ICE |
| `pickit4` | MPLAB PICkit 4 |
| `powerdebugger` | MPLAB Power Debugger |
| `jtagice3` | JTAGICE3 |
| `edbg` | EDBG probe (Xplained boards) |
| `medbg` | mEDBG (Xplained Mini) |
| `nedbg` | nEDBG (Curiosity Nano) |
| `dwlink` | UNO-based [dw-link](https://github.com/felias-fogg/dw-link) serial probe (pass-through) |

In addition, **`simavr`** can be driven as a simulated target via `-s simavr` (no probe needed).

## Microcontrollers

PyAvrOCD ships **~280 device definitions** (one Python module per part in `pyavrocd/deviceinfo/devices/`). Coverage spans:

- **Classic AVR** — ATtiny (e.g. `attiny85`, `attiny2313a`, `attiny841`) and ATmega (e.g. `atmega168`, `atmega328p`, `atmega640`, `atmega1284`) via debugWIRE / JTAG.
- **Modern tinyAVR / megaAVR-0** — e.g. `attiny404`, `attiny3226`, `attiny406` via UPDI.
- **AVR Dx / Ex** — e.g. `avr64db48`, `avr32ea48`, `avr16eb20`, `avr32da28` via UPDI.
- **AT90 / specialty parts** — e.g. `at90can128`, `at90pwm2b`, `atmega16m1`, `atmega32hvb`.

To see the authoritative list for your installed version:

```bash
pyavrocd -d ?                    # all supported MCUs
pyavrocd -d ? -i updi            # only those reachable via UPDI
```

The upstream docs also publish browsable lists of [supported MCUs](https://pyavrocd.io/supported-mcus/), [supported boards](https://pyavrocd.io/supported-boards/), and [supported debuggers](https://pyavrocd.io/supported-debuggers/).

## Notes & limitations

- Programs compiled with `-mrelax` cannot be debugged; PyAvrOCD detects this from the ELF file and refuses (`--elf-file`).
- Hardware breakpoints are limited per architecture; PyAvrOCD mixes hardware and software breakpoints (configurable via `monitor breakpoints`).
- Xmega (PDI) support is partial — extending it is an open roadmap question (see [[Project Status]]).
