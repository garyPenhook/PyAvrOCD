# Project Status

_Last updated: 2026-06-01_

## Current version

| Item | Value |
|------|-------|
| **Version** | **1.5.1** |
| Released | 01-Jun-2026 (upstream tag `v1.5.1`) |
| Fork | [`garyPenhook/PyAvrOCD`](https://github.com/garyPenhook/PyAvrOCD) |
| Upstream | [`felias-fogg/PyAvrOCD`](https://github.com/felias-fogg/PyAvrOCD) |
| `main` HEAD | `321b968` (merge of upstream `v1.5.1` + fork changes) |
| Python | 3.10 – 3.14 |
| License | MIT |
| Development status | Production/Stable |

## What's in 1.5.1

- **Added** — new `monitor ioregister` command. With one argument it matches I/O register names by wildcard and prints matched registers, their values, and bitfields; a unique match also prints its bitfields. With a second (integer) argument it writes that value into the addressed register or bitfield.
- **Added** — `deviceinfo/addsvd.py` utility that reads an SVD file and embeds it as a Python data structure in the matching device file (run after `harvest.py`).
- **Changed** — `sram_masked_read` / `sram_masked_write` moved into `xavrdebugger` so they can be reused by the monitor command.
- **Fixed** — read/write masking now works because the read-only / write-only register lists are populated after `device_info` is read.

> Note: 1.5.0 was yanked upstream because the announced functionality did not work; 1.5.1 is the effective successor to 1.4.0.

## How this fork differs from upstream

This fork tracks upstream and adds local tooling changes:

1. **Build/dev tooling migrated from Poetry to `uv`** — dependency resolution and the dev environment are managed with [uv](https://docs.astral.sh/uv/); see `pyproject.toml` and `uv.lock`.
2. **Pylint workflow** — a GitHub Actions Pylint workflow was added and tuned for this project.

Upstream `v1.5.1` has been merged into `main`, and `main` is pushed to the fork's `origin`. No pull request is opened against upstream.

### Keeping in sync with upstream

```bash
git remote add upstream https://github.com/felias-fogg/PyAvrOCD.git   # one-time
git fetch upstream --tags
git merge upstream/main          # or: git merge v<x.y.z>
uv lock && uv sync               # refresh the environment for the new version
```

## Continuous integration

The fork carries these GitHub Actions workflows (`.github/workflows/`):

| Workflow | Purpose |
|----------|---------|
| `unit-tests.yml` | Run the pytest unit suite |
| `unit-tests-matrix.yml` | Unit tests across Python versions / OSes |
| `pylint.yml` | Static analysis with Pylint (fork addition) |
| `create-badge.yml` | Generate pylint/pytest/coverage badges |
| `build-binaries.yml` | Build standalone binaries via PyInstaller |
| `release.yml` | Publish releases |

## Roadmap (from upstream)

- Coverage now spans all debugWIRE, JTAG (megaAVR), and UPDI MCUs.
- Considering whether to extend coverage to **Xmega** parts.
- Idea to rebase the toolchain assumptions on **more recent GCC** versions to resolve several debugging-front issues.
- Ongoing intent to fix some of the more obvious bugs in GDB's AVR support.

## At a glance

- **~280** device definition files under `pyavrocd/deviceinfo/devices/`.
- **~7,750** lines of Python in the `pyavrocd/` package.
- Unit tests plus an end-to-end test harness under `tests/`.
