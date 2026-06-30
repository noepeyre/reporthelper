# Report Helper

Report Helper is a small Windows Python tool controlled with global hotkeys. It automates a repeated three-click workflow in a graphical application by using layout reference files.

French README: [READMEfr.md](READMEfr.md).

## Quick Start

For a complete setup guide, see [INSTALL.md](INSTALL.md). A French version is available in [INSTALLfr.md](INSTALLfr.md).

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Hotkeys

- `F8` opens the configuration window, only when automation is stopped.
- `F10` starts or stops automation immediately.
- `F9` exits the program cleanly.

When the app starts, it does nothing until the configuration has been opened and saved at least once with `F8`.

## Configuration

In the `F8` window, choose:

- the target slot;
- the number of menu options;
- the option to select;
- the loop count;
- the speed in milliseconds;
- the random offset in pixels;
- the layout to use.

The layout is loaded from a reference file shipped with the project, such as `layout_reference.json` or `layout_reference_v2.json`.
