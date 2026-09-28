# SerialRenamer — Documentation

## 1. Overview

SerialRenamer renames all files in a folder to sequential integers,
preserving each file's original extension. There are two independent
implementations, provided for different needs:

| File | Purpose |
|---|---|
| `SerialRenamer.bat` | Standalone renamer — pure batch, no Python needed |
| `File_name Changer.py` | Core renaming logic (Python version) |
| `Run File Name Changer.bat` | Windows double-click launcher for the Python version |
| `README.md` | Quick start / GitHub landing page |
| `DOCUMENTATION.md` | This file — detailed reference |

Both implementations follow the same behavior spec (section 2) and share
the same limitations (section 3).

## 2. SerialRenamer.bat (standalone version)

This is a single, self-contained `.bat` file — copy it into any folder and
double-click it. No Python, no second file to bring along.

```bat
@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "self=%~nx0"
set "counter=1"

for /f "delims=" %%F in ('dir /b /a-d /on') do (
    if /I not "%%F"=="!self!" (
        set "ext=%%~xF"
        echo Renaming: %%F -^> !counter!!ext!
        ren "%%F" "!counter!!ext!"
        set /a counter+=1
    )
)

set /a renamed=!counter!-1
echo.
echo Done. Renamed !renamed! file(s).
pause
endlocal
```

How it works:

- `cd /d "%~dp0"` moves into the batch file's own folder first, so behavior
  doesn't depend on where it's launched from.
- `dir /b /a-d /on` lists files only (`/a-d` excludes directories) in
  ascending name order (`/on`) — the same alphabetical-first ordering as
  the Python version.
- `%~nx0` is the batch file's own name, used to skip itself.
- `%%~xF` extracts each file's extension (including the leading dot).
- `pause` keeps the console window open so you can read the log.

Batch-scripting note: avoid using `!` in `echo` strings elsewhere in this
file. With `setlocal enabledelayedexpansion`, `!` is a special character
used to delimit variable references — an odd number of `!` characters on a
line (e.g. `echo Done! Renamed !renamed! file(s).`) causes the parser to
misinterpret text between them, silently dropping words. This is why the
summary line reads "Done." rather than "Done!".

## 3. Behavior specification

Given a directory `D` containing the script:

1. Build the list of entries in `D` where:
   - the entry is a file (not a directory), **and**
   - the entry is not the script itself.
2. Sort that list alphabetically (case-sensitivity follows the OS's default
   string sort — on Windows this is effectively case-insensitive for
   typical filenames).
3. Starting from `counter = 1`, for each file in sorted order:
   - Extract its extension (e.g. `.jpg`, `.txt`; no extension → empty
     string).
   - Compute the new name as `f"{counter}{extension}"`.
   - Rename the file via `os.rename`.
   - Increment `counter`.
4. Print a per-file rename log line and a final summary count.

### Not handled / known limitations

- **No recursion**: files in subfolders are ignored entirely.
- **No collision protection**: if a file already happens to be named e.g.
  `5.png`, and another `.png` file later in the sort order gets renamed to
  `5.png` by the counter, `os.rename` will silently overwrite the original
  `5.png`. **Back up the folder before running.**
- **No undo / rename log persisted to disk**: the mapping from old name to
  new name is only printed to the console, not saved to a file.
- **Errors are caught per-file**: if one rename fails (e.g. file is open
  elsewhere / permissions issue), the script prints an error and continues
  with the next file rather than aborting.

## 4. Requirements

- **`SerialRenamer.bat`**: Windows only, no dependencies — `cmd.exe` is
  built in.
- **`File_name Changer.py`**: Python 3.6+ (uses f-strings and `pathlib`; no
  third-party packages). Cross-platform — Linux/macOS users can run it
  directly with `python3`.
- **`Run File Name Changer.bat`**: Windows only, and requires Python on
  `PATH` (since it just calls the `.py` script).

## 5. Setup

- **Standalone `.bat`**: copy `SerialRenamer.bat` alone into the target
  folder. Nothing else to install or place alongside it.
- **Python version**: place `File_name Changer.py` (and, on Windows,
  `Run File Name Changer.bat`) inside the folder whose files you want
  renamed, then ensure Python is installed and on `PATH`:
  ```powershell
  python --version
  ```
  If this fails, install Python from https://python.org and re-check
  "Add python.exe to PATH" during setup.

## 6. Running

### Standalone batch file (Windows)

Double-click `SerialRenamer.bat` directly in the target folder — see
section 2 for what it does internally.

### Python launcher (Windows)

Double-click `Run File Name Changer.bat`. It:

```bat
@echo off
cd /d "%~dp0"
python "File_name Changer.py"
pause
```

- `cd /d "%~dp0"` moves into the batch file's own folder first, so it works
  regardless of where it's launched from.
- `pause` keeps the console window open after completion so you can read
  the log before it closes.

### Command line (any OS)

```bash
cd path/to/target/folder
python "File_name Changer.py"
```

## 8. Extending the scripts

### Python version (`File_name Changer.py`)

- **Recurse into subfolders**: replace the `os.listdir` call with
  `os.walk(root_path)` and rename within each directory tuple returned.
- **Zero-padded numbers** (`001.jpg` instead of `1.jpg`): change
  `new_name = f"{counter}{extension}"` to
  `new_name = f"{counter:03d}{extension}"` (adjust the width as needed).
- **Sort by modification time instead of name**: replace the `sorted(...)`
  key with `key=lambda f: (root_path / f).stat().st_mtime`.
- **Write a rename log to disk**: append each `(old_name, new_name)` pair
  to a CSV before/while renaming, so the operation can be reversed later.

### Standalone version (`SerialRenamer.bat`)

- **Zero-padded numbers**: change `set /a counter+=1` initial value and
  format manually, e.g. build a 3-digit string with
  `set "padded=00!counter!"` then take the last 3 characters
  (`!padded:~-3!`) before using it in the new name.
- **Sort by modification time**: change `dir /b /a-d /on` to
  `dir /b /a-d /o-d` (newest first) or `/od` (oldest first) — note `/o-d`
  and `/od` sort by modification time, not name.
- Recursion and a persisted rename log are both significantly more
  fiddly in batch than in Python; if you need either, prefer editing the
  Python version instead.

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Double-clicking `Run File Name Changer.bat` flashes and closes immediately | `python` not on `PATH` | Install Python / add it to `PATH`; the `pause` line should otherwise keep the window open — if it still closes instantly, `python` itself isn't being found |
| `PermissionError` (Python) / rename silently fails (batch) | File is open in another program, or read-only | Close the file elsewhere, or remove the read-only attribute |
| Files renamed in an unexpected order | Sorting is alphabetical, not by date | See "Extending the scripts" to sort by modification time instead |
| `SerialRenamer.bat`'s summary line looks garbled | Stray `!` characters in an edited `echo` line, misparsed under `enabledelayedexpansion` | Keep an even number of `!` per line, or avoid `!` in literal text entirely (see section 2) |

## 10. License

Not yet specified. Add a `LICENSE` file (MIT is a common permissive choice
for small utilities like this) before publishing publicly if you want to
make usage terms explicit.
