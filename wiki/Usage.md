# Usage

PyAvrOCD runs as a GDB server: you start it, point it at a target MCU and a debug probe, then connect with `avr-gdb`.

## Basic workflow

```bash
# 1. Start the server (example: ATmega328P via an MPLAB Snap on the default port 2000)
pyavrocd -d atmega328p -t snap

# 2. In another terminal, launch GDB and connect
avr-gdb my_sketch.elf
(gdb) target remote :2000
(gdb) load
(gdb) break loop
(gdb) continue
```

If no debug probe is found and `-t dwlink` is selected (or no EDBG tool is present), PyAvrOCD falls back to the serial `dw-link` pass-through. Use `-s simavr` to debug against the simulator instead of hardware.

Tip: arguments can also be read from a file — if a `pyavrocd.options` file exists in the working directory it is appended automatically, and `@file` syntax includes any file's contents as arguments.

## Command-line options

| Option | Argument | Description |
|--------|----------|-------------|
| `-d`, `--device` | name / `?` | Target MCU to debug; `-d ?` lists all supported MCUs (combine with `-i` to filter by interface). |
| `-t`, `--tool` | name / `?` | Debug probe to use: `atmelice`, `dwlink`, `edbg`, `jtagice3`, `medbg`, `nedbg`, `pickit4`, `powerdebugger`, `snap`. |
| `-i`, `--interface` | name / `?` | Force a debug interface: `debugwire`, `jtag`, `pdi`, `updi` (otherwise auto-detected from the device). |
| `-u`, `--usbsn` | serial | Select a specific probe by USB serial number (when several are connected). |
| `-p`, `--port` | int | Local TCP port for GDB (default **2000**). |
| `-a`, `--attach` | — | Attach without resetting the MCU. |
| `-e`, `--elf-file` | file | ELF file to check; debugging is refused if it was built with `-mrelax`. |
| `-m`, `--manage` | fuse / `?` | Fuses PyAvrOCD may change. Repeatable. Values: `all`, `none`, `bootrst`, `dwen`, `ocden`, `lockbits`, `eesave` and their `no…` negations (default `none`). |
| `-F`, `--F_CPU` | Hz | CPU clock frequency in Hz (default `1000000`). |
| `-C`, `--comm-speed` | kbps | (U)PDI communication speed in kbps (default `750`). |
| `-D`, `--debug-clock` | kHz | JTAG clock for debugging (default `200`). |
| `-P`, `--prog-clock` | kHz | JTAG clock for programming (default `1000`). |
| `-s`, `--start` | prog | Start a helper program; `-s simavr` runs the simulator instead of hardware. |
| `-x`, `--xargs` | args | Extra arguments passed to `simavr`. |
| `-v`, `--verbose` | level / `?` | Log level: `all`, `debug`, `info`, `warning`, `error`, `critical` (default `info`). |
| `-V`, `--version` | — | Print the PyAvrOCD version and exit. |
| `-H`, `--webhelp` | — | Open the online command-line reference in a browser. |

Full reference: [pyavrocd.io/command-line-options](https://pyavrocd.io/command-line-options/).

## `monitor` commands

From the GDB prompt, `monitor <cmd>` controls server-side behavior. Available commands:

| Command | What it does |
|---------|--------------|
| `monitor help` | List available monitor commands. |
| `monitor info` | Show session / target information. |
| `monitor version` | Show the PyAvrOCD version. |
| `monitor reset` | Reset the target MCU. |
| `monitor breakpoints` | Choose breakpoint policy (all / hardware-only / software-only). |
| `monitor singlestep` | Select safe vs. plain single-stepping (interrupt protection). |
| `monitor rangestepping` | Enable/disable GDB range-stepping (speeds up stepping). |
| `monitor caching` | Enable/disable the flash cache used to reduce flash wear. |
| `monitor load` | Control load behavior: read-before-write / write-only / no initial load. |
| `monitor erasebeforeload` | Erase flash before loading (default on JTAG targets). |
| `monitor onlywhenloaded` | Require a prior `load` before execution (disable to run as-is). |
| `monitor verify` | Verify flash contents after loading. |
| `monitor timers` | Freeze or run timers while execution is stopped. |
| `monitor atexit` | Behavior on exit (e.g. stay in / leave debugWIRE mode). |
| `monitor debugwire` | Enable/disable debugWIRE mode (DWEN fuse) on classic targets. |
| `monitor ioregister [name [value]]` | **(new in 1.5.1)** Match I/O registers by name (wildcards); print matched registers/bitfields and their values. A unique match prints its bitfields; supply an integer `value` to write it to the addressed register or bitfield. |

Many of these mirror command-line options, so you can set defaults at startup and adjust them live during a session. See [pyavrocd.io/monitor-commands](https://pyavrocd.io/monitor-commands/) for full details.
