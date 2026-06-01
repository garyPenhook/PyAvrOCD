# Development

This page covers building, testing, and contributing to the `garyPenhook/PyAvrOCD` fork. Tooling here uses [uv](https://docs.astral.sh/uv/) (migrated from Poetry in this fork).

## Environment setup

```bash
git clone https://github.com/garyPenhook/PyAvrOCD.git
cd PyAvrOCD
uv sync --group dev        # install runtime + dev dependencies into .venv
```

Dev dependencies include `pre-commit`, `pyinstaller`, `pytest`, and the linters used by CI.

## Running the test suite

```bash
uv run pytest                       # full unit-test suite
uv run pytest tests/test_memory.py  # a single module
```

Unit tests live in `tests/` (e.g. `test_gdbhandler.py`, `test_breakandexec*.py`, `test_memory.py`, `test_xnvm*.py`, `test_xavr8target_*.py`). There is also an **end-to-end** harness under `tests/end-to-end/` (`e2e_tests.py`, `serv.sh`, `scripts.py`, `devices.py`) that exercises real targets/boards. See `tests/README.md` for details.

## Linting and type checking

```bash
uv run pylint pyavrocd             # static analysis (CI: pylint.yml)
uv run pre-commit run --all-files  # run all configured pre-commit hooks
```

The project is type-annotated and checked with mypy (the `:my[py]: checked` badge). The fork added and tuned the Pylint GitHub Actions workflow.

## Building a standalone binary

```bash
uv run pyinstaller pyavrocd.spec
```

CI does this in `build-binaries.yml`; the `pyavrocd.spec` file defines the PyInstaller bundle.

## Repository layout

```
pyavrocd/             # the package (see Architecture page)
  deviceinfo/
    devices/          # ~280 per-MCU definition modules
    harvest.py        # generate device modules
    addsvd.py         # embed SVD data into device modules (run after harvest)
svd/                  # SVD source files for the devices
tests/                # unit tests + end-to-end harness
docs/                 # MkDocs site sources (pyavrocd.io)
examples/             # sample sketches (Arduino .ino, PlatformIO)
extras/, pcbs/        # supporting material and probe hardware
pyproject.toml        # project metadata + deps (uv)
uv.lock               # locked dependency set
pyavrocd.spec         # PyInstaller build spec
```

## Regenerating device data

When adding or updating MCU support:

1. Run `harvest.py` to (re)generate the device module(s) under `deviceinfo/devices/`.
2. Run `addsvd.py` to embed the corresponding SVD data (from `svd/`) into those modules.

## Adding a new device's SVD

The new (1.5.1) `addsvd.py` utility reads an SVD file and writes it as a Python data structure into the matching device file. This is what powers register/bitfield introspection in `monitor ioregister`.

## Contributing

This fork tracks upstream [felias-fogg/PyAvrOCD](https://github.com/felias-fogg/PyAvrOCD). For changes intended for the broader project, follow the upstream [contributing guide](https://pyavrocd.io/contributing/) and open PRs there. Fork-specific changes (tooling, CI) stay on this fork's `main`.

See [[Project Status]] for how to merge new upstream releases into the fork.
