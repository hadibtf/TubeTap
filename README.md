# YouTube Downloader Telegram Bot

A simple yet powerful Telegram bot built with Python and `aiogram` to download YouTube videos as MP4 or MP3 files. It uses `yt-dlp` for downloading and `ffmpeg` for media conversion.

## Features

- **YouTube Video Downloading**: Fetches videos directly from any valid YouTube URL.
- **MP3 Audio Conversion**: Extracts and converts video content to high-quality MP3 audio.
- **MP4 Video Output**: Provides direct downloads of videos in MP4 format.
- **Duration Limit**: Politely rejects videos longer than 10 minutes to conserve resources.
- **User-Friendly Interaction**:
  - Sends a "Downloading..." message to acknowledge the request.
  - Replaces the status message with the final file upon completion.
- **Request Logging**: Logs every download request to standard output with a timestamp, URL, and file size for easy monitoring.
- **Modular Architecture**: The code is cleanly organized into separate modules for bot logic, message handling, and download processing.

## Prerequisites

Before you begin, ensure you have the following installed on your system (e.g., a Debian VM):

- **Python 3.8+**
- **pip** (Python package installer)
- **FFmpeg**: A command-line tool for handling multimedia data.

## Installation & Setup

Follow these steps to get the bot up and running.

### 1. Clone the Repository

First, get the project files onto your machine. If you have git installed:
```bash
git clone <repository-url>
cd <repository-directory>
```
If not, simply download the source files (`main.py`, `handlers.py`, `downloader.py`, `requirements.txt`, `.env`) into a new directory.

### 2. Install FFmpeg

On Debian-based systems like Ubuntu, you can install FFmpeg with `apt`:
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```
For other operating systems, please refer to the [official FFmpeg download page](https://ffmpeg.org/download.html).

### 3. Install Python Dependencies

Install all the required Python libraries using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 4. Configure the Bot Token

The bot requires a Telegram Bot Token to authenticate with the Telegram API.

1.  **Get a Token**: Talk to the [BotFather](https://t.me/BotFather) on Telegram to create a new bot and receive your unique token.
2.  **Set the Token**: Open the `.env` file and replace `YOUR_BOT_TOKEN` with the token you received.
    ```env
    BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123456789
    ```

## How to Run the Bot

Once the setup is complete, you can start the bot with a single command:

```bash
python3 main.py
```

If everything is configured correctly, you will see the log message "Starting bot..." in your terminal. The bot is now active and listening for messages.

## How to Use the Bot

Open a chat with your bot on Telegram and use the following commands:

-   **`/start`**
    Displays a welcome message.

-   **`/mp3`**
    The bot will ask for a YouTube URL. Send the URL in the next message, and the bot will download the video and send it back as an MP3 audio file.

-   **`/mp4`**
    The bot will ask for a YouTube URL. Send the URL in the next message, and the bot will download the video and send it back as an MP4 video file.

If you send a URL for a video that is longer than 10 minutes, the bot will respond with a message indicating that the video is too long and will not proceed with the download.

## Project Structure

The project is organized into several files to keep the code clean and maintainable:

```
.
├── .env              # Stores environment variables like the BOT_TOKEN
├── main.py           # The main entry point of the application. Initializes and starts the bot.
├── handlers.py       # Defines all message handlers and bot command logic.
├── downloader.py     # Contains functions for downloading videos and converting them with yt-dlp/ffmpeg.
└── requirements.txt  # Lists all Python dependencies for the project.
```

---

Feel free to fork this project, submit issues, and contribute to its development.
