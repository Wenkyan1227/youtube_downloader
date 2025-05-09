# YouTube Downloader Web

This is a web application that allows users to download YouTube videos and audio files by providing URLs. The application supports downloading videos in various formats and converting audio files to MP3.

## Features

- **Download YouTube Videos**: Users can download YouTube videos by pasting the video URL.
- **Download Audio**: Users can download the audio from YouTube videos in the best available quality.
- **Audio Conversion**: Audio files are automatically converted to MP3 format for easier use.
- **Excel Support**: Users can upload an Excel file containing YouTube video links to download multiple videos/audio at once.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript (jQuery)
- **Database**: N/A (Local file system used for storing downloads)
- **Libraries/Tools**:
  - `yt-dlp` for downloading videos and audio.
  - `FFmpeg` for converting audio files to MP3.
  - `openpyxl` for handling Excel file input.

## Installation

### Prerequisites

- Python 3.x
- `yt-dlp`
- `FFmpeg`
- Flask

### Steps

1. Clone this repository:

   ```bash
   git clone https://github.com/Wenkyan1227/youtube_downloader.git
