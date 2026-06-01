# Installation

PyAvrOCD is a Python application (Python 3.10–3.14). The official, easiest installation paths are documented at [pyavrocd.io/install](https://pyavrocd.io/install/). This page covers the common options and the fork's `uv`-based developer setup.

## Option 1 — Install from PyPI

```bash
pip install pyavrocd
pyavrocd --version        # should print: PyAvrOCD version 1.5.1
```

A standalone binary (no Python required) is also published for each release on the upstream [Releases page](https://github.com/felias-fogg/PyAvrOCD/releases), built by the `build-binaries` workflow.

## Option 2 — Run this fork from source (with `uv`)

This fork uses [uv](https://docs.astral.sh/uv/) for environment and dependency management.

```bash
git clone https://github.com/garyPenhook/PyAvrOCD.git
cd PyAvrOCD
uv sync                   # create the venv and install deps from uv.lock
uv run pyavrocd --version
```

`uv sync` installs the project plus its locked dependencies (`pymcuprog`, `pyedbglib`, `pyusb`, `pexpect`, `pyelftools`, `svd2py`). Use `uv sync --group dev` to also install the development tools (pre-commit, pyinstaller, pytest, etc.).

## Platform prerequisites

PyAvrOCD talks to USB debug probes via libusb. If probe discovery fails:

- **Linux** — `sudo apt install libusb-1.0-0`, and install the udev rules so non-root users can access EDBG probes. Download [`99-edbg-debuggers.rules`](https://pyavrocd.io/99-edbg-debuggers.rules), review it, and place it in `/etc/udev/rules.d/`, then reload udev.
- **macOS** — `brew install libusb`.
- **Windows** — USB core is not used (HID access is built in); no libusb step is needed.

## Verifying the install

```bash
pyavrocd -d ?             # list all supported MCUs
pyavrocd -t ?             # list supported debug probes
pyavrocd -i ?             # list debug interfaces
```

## Editor / IDE integration

PyAvrOCD is designed to plug into **Arduino IDE 2** and **PlatformIO**. The upstream docs include quickstart guides for:

- Arduino IDE 2 (UNO, ATtiny, Xmini, generic) — see [pyavrocd.io/quick_arduino](https://pyavrocd.io/quick_arduino/)
- PlatformIO (ATtiny, ATmega1284, Curiosity Nano, generic) — see the `quick_pio*` docs

See [[Usage]] for how GDB connects to the running server.
