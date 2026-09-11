# Video Downloader GUI

[![Tests](https://github.com/TimurPanin/video-downloader-gui/actions/workflows/tests.yml/badge.svg)](https://github.com/TimurPanin/video-downloader-gui/actions/workflows/tests.yml)

Desktop video downloader for **YouTube** and **TikTok**, built with **Python, Tkinter and yt-dlp**.

The project provides a Windows-oriented graphical interface for common download workflows while keeping download logic, URL validation, configuration, cookies handling and UI pages separated into dedicated modules.

> Use this application only for content you are authorized to download and in accordance with the applicable platform terms and local law.

## Status

**Public portfolio project / working desktop application.**

The current version supports YouTube and TikTok workflows, configurable download options, RU/EN interface text and Windows packaging with PyInstaller.

## Features

- YouTube single-video downloads
- YouTube playlist detection and playlist downloads
- TikTok video downloads
- Video quality presets: Best, 1080p, 720p, 480p and 360p where available
- Audio-only MP3 extraction through FFmpeg
- Download progress reporting
- Configurable download directory
- Download speed limit and concurrent-fragment settings
- Browser/session cookie support
- Russian and English interface text
- Persistent local settings
- Windows executable build script
- Unit tests for URL validation, configuration, language strings and YouTube mode detection

## Tech stack

- **Python 3**
- **Tkinter / ttk**
- **yt-dlp**
- **FFmpeg** for audio post-processing
- **browser-cookie3**
- **requests**
- **unittest**
- **PyInstaller** for Windows packaging

## Project structure

```text
video-downloader-gui/
├── app.py                  # Main Tkinter application
├── run.py                  # Convenience launcher
├── build.py                # Windows/PyInstaller build helper
├── core/
│   ├── config.py           # Persistent application settings
│   ├── cookies.py          # Cookie/session handling
│   ├── downloader.py       # yt-dlp integration
│   ├── i18n.py             # Interface translations
│   └── validation.py       # URL validation
├── pages/
│   ├── menu.py             # Main menu
│   ├── loader_youtube.py   # YouTube workflow
│   └── loader_tiktok.py    # TikTok workflow
├── test_app.py             # unittest test suite
├── requirements.txt
└── LICENSE
```

## Run locally

### Requirements

- Python 3.10+
- Windows 10/11 recommended for the current desktop workflow
- FFmpeg available in `PATH` for MP3 extraction

### Installation

```bash
git clone https://github.com/TimurPanin/video-downloader-gui.git
cd video-downloader-gui
python -m venv .venv
```

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python run.py
```

You can also launch the main module directly:

```bash
python app.py
```

## Tests

```bash
python test_app.py
```

The current test suite covers URL validation, application configuration, RU/EN translation strings and YouTube single/playlist mode detection. The repository also runs the suite automatically on Windows through GitHub Actions.

## Build for Windows

The repository includes `build.py`, which installs/checks the required build dependencies and invokes PyInstaller.

```bash
python build.py
```

The resulting executable is written to:

```text
dist/VideoDownloader.exe
```

FFmpeg still needs to be available to the application for audio conversion.

## Configuration

Application settings are stored locally in:

```text
%USERPROFILE%/.vd_settings.json
```

Current settings include the download directory, rate limit, concurrent fragments, output filename template, cookie preferences, last page and interface language.

## Architecture notes

`core/downloader.py` encapsulates yt-dlp configuration and background download execution. The UI is split into separate menu, YouTube and TikTok pages, while configuration, URL validation, localization and cookies handling live in dedicated modules.

This keeps the desktop interface separate from the download and configuration logic and makes the project easier to extend than a single-file GUI script.

## Additional documentation

- [Usage](USAGE.md)
- [Build notes](BUILD.md)
- [Changelog](CHANGELOG.md)

## License

Licensed under the [MIT License](LICENSE).
