# GodTyper

A Python utility that types out the contents of any file when you press F1.

## Features

- Type out any text or code file with a customizable typing speed
- Human-like typing variations (can be disabled)
- Simple keyboard shortcut (F1) to start typing
- Works with any file extension

## Requirements

- Python 3
- keyboard package (`pip install keyboard`)

## Installation

1. Clone or download this repository
2. Install the required package:
   ```
   pip install keyboard
   ```
3. Make the script executable (Linux/Mac):
   ```
   chmod +x godtyper.py
   ```

## Usage

```
python godtyper.py [file_path] [--wpm WPM] [--no-humanize]
```

### Arguments

- `file_path`: Path to the file you want to type out
- `--wpm`: Words per minute typing speed (default: 60)
- `--no-humanize`: Disable human-like typing variations

### Example

```
python godtyper.py example.py --wpm 80
```

### How to Use

1. Run the script with your desired file and WPM
2. Switch to the application where you want the text to be typed
3. Press F1 to start typing
4. Press Ctrl+C at any time to stop typing

## Notes

- The script requires keyboard access permissions, which may require running with administrator/sudo privileges on some systems
- Be careful when typing large files as there is no built-in undo functionality
- The WPM calculation is based on an average of 5 characters per word