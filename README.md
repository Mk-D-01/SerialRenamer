# SerialRenamer

A tiny Windows utility that renames every file in a folder to sequential
numbers (`1.jpg`, `2.jpg`, `3.png`, ...), keeping each file's original
extension.

## Why

Useful for cleaning up folders full of inconsistently named files (camera
dumps, downloads, scanned pages, etc.) where you just want them numbered in
order.

## How it works

- The script only touches files that sit **directly inside the same folder
  it's run from** — subfolders are left alone.
- It skips itself, so it's safe to keep the script in the folder you're
  renaming.
- Files are sorted alphabetically first, then numbered starting at `1`.
- Each file keeps its original extension.

## Usage

### Option 1: Standalone batch file (recommended — no Python required)

1. Copy **`SerialRenamer.bat`** into the folder whose files you want renamed.
2. Double-click it.
3. A console window shows each rename and stays open at the end so you can
   review the output.

This is a single, self-contained file — no Python install needed, nothing
else to copy alongside it.

### Option 2: Python script + launcher

1. Copy `File_name Changer.py` and `Run File Name Changer.bat` into the
   folder whose files you want renamed.
2. Double-click **`Run File Name Changer.bat`**.

Requires Python to be installed and available on your system `PATH`.

### Option 3: Run the Python script from a terminal

```bash
python "File_name Changer.py"
```

Run it from inside the target folder, or place the script in that folder
first — it always operates on its own directory, not the current working
directory.

## ⚠️ Warning

Renaming is **irreversible** — original filenames are not recorded anywhere.
Test on a copy of your files first, or make sure you have a backup before
running this on anything important.

## Requirements

- Windows (the `.bat` launcher is Windows-specific; the Python script itself
  is cross-platform)
- Python 3.6+ (no external dependencies)

## License

No license specified yet — add one (e.g. MIT) if you plan to share this
publicly.
