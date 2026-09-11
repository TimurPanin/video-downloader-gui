# Building Video Downloader GUI

This document describes the current Windows build process for `VideoDownloader.exe`.

## Requirements

- Windows 10 or 11
- Python 3.10+
- `pip`
- FFmpeg available in `PATH` for MP3 extraction at runtime

## Recommended build

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the build helper:

```bash
python build.py
```

The script checks the project dependencies, installs PyInstaller when necessary, builds the executable and removes temporary PyInstaller files after a successful build.

The resulting executable is written to:

```text
dist/VideoDownloader.exe
```

## Manual PyInstaller build

The equivalent basic command is:

```bash
python -m pip install pyinstaller
pyinstaller --onefile --noconsole --name VideoDownloader --distpath dist --workpath build --specpath . app.py
```

The application modules under `core/` and `pages/` are imported by the Python application and are collected by PyInstaller through the normal import graph.

## Validate the build

After building:

1. Confirm that `dist/VideoDownloader.exe` exists.
2. Start the executable.
3. Open the YouTube and TikTok pages.
4. Confirm that settings and language switching work.
5. Confirm that FFmpeg is available before testing MP3 extraction.

## FFmpeg

FFmpeg is not bundled by `build.py`. It must be available to the application at runtime when audio conversion is requested.

If FFmpeg is installed but the application cannot find it, verify that the FFmpeg `bin` directory is included in the Windows `PATH` environment variable and restart the application.

## Troubleshooting

### PyInstaller is missing

`build.py` installs PyInstaller automatically when it is not available. You can also install it manually:

```bash
python -m pip install pyinstaller
```

### A dependency is missing

Reinstall the project dependencies:

```bash
python -m pip install -r requirements.txt
```

### Build fails

Run the test suite first:

```bash
python test_app.py
```

Then run the build helper again and inspect the error output printed by `build.py`.

## Distribution note

The executable is a project build artifact, not a signed installer. If the application is distributed to other users, document the FFmpeg requirement and test the executable on a clean Windows environment first.
