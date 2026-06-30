# Installation Guide

This guide explains how to install and run Report Helper on Windows with PowerShell.

## 1. Install Python and pip

1. Open this page in your browser: <https://www.python.org/downloads/windows/>
2. Download the latest stable Python 3 installer for Windows.
3. Run the installer.
4. On the first installer screen, enable **Add python.exe to PATH**.
5. Click **Install Now**.

Recent Python installers include `pip`. After installation, open a new PowerShell window and check both commands:

```powershell
python --version
python -m pip --version
```

If `pip` is missing, run:

```powershell
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

## 2. Download the Project

Download the project from GitHub, then extract it if you downloaded a ZIP file.

If you use Git, run:

```powershell
git clone https://github.com/YOUR-USERNAME/reporthelper.git
cd reporthelper
```

If you downloaded a ZIP file, open PowerShell in the extracted project folder.

## 3. Create a Virtual Environment

From the project folder, run:

```powershell
python -m venv .venv
```

This creates a local Python environment in the `.venv` folder.

## 4. Activate the Virtual Environment

PowerShell may block script activation by default. To allow activation only for the current PowerShell window, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

When activation works, your prompt usually starts with `(.venv)`.

## 5. Install Dependencies

With the virtual environment active, install the required packages:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 6. Run Report Helper

Start the app:

```powershell
python main.py
```

The console should show that Report Helper is ready.

## 7. Use the Hotkeys

- Press `F8` to open the configuration window.
- Choose the target slot, menu option count, option to select, loop count, speed, random offset, and layout file.
- Click **Save**.
- Press `F10` to start automation.
- Press `F10` again to stop automation.
- Press `F9` to quit the program.

The app stays inactive until you open and save the configuration at least once with `F8`.

## 8. Troubleshooting

If `python` is not recognized, close PowerShell, open a new PowerShell window, and try again. If it still fails, reinstall Python and make sure **Add python.exe to PATH** is enabled.

If activation is blocked, run this command in the same PowerShell window before activating:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

If dependencies fail to install, upgrade `pip` and retry:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the hotkeys do not work, make sure the PowerShell window running `python main.py` is still open. Some systems may require running PowerShell normally from the desktop session rather than from a restricted terminal.

## 9. Updating Later

If you installed with Git, update the project with:

```powershell
git pull
```

Then reactivate the virtual environment and reinstall dependencies if needed:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
