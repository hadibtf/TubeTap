
# TubeTap 🎧

A Telegram bot built with Python that lets you download YouTube audio (MP3) or video (MP4) on demand.  
It uses **aiogram** for Telegram integration and **yt-dlp** + **FFmpeg** for media handling.  
Supports restricted content via cookie-based authentication.

---

## 📋 Table of Contents

- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [1. BotFather & Bot Token](#1-botfather--bot-token)  
- [2. Local Setup](#2-local-setup)  
- [3. Cookie Authentication](#3-cookie-authentication)  
- [4. Running Locally](#4-running-locally)  
- [5. VPS Deployment Guide](#5-vps-deployment-guide)  
  - [5.1 System Installation (Ubuntu)](#51-system-installation-ubuntu)  
  - [5.2 Install Google Chrome](#52-install-google-chrome)  
  - [5.3 Deploy & Run](#53-deploy--run)  
- [6. Usage](#6-usage)  
- [7. Troubleshooting](#7-troubleshooting)  
- [8. Git Workflow & Contributing](#8-git-workflow--contributing)  
- [9. License](#9-license)

---

## Features

- **MP3 Download**: Extract audio from YouTube links.  
- **MP4 Download**: Save full video in MP4 format.  
- **Restricted Content**: Use your own `cookies.txt` to download age‑restricted or sign‑in‑required videos.  
- **Clean FSM Flow**: `/start` → send link → choose MP3/MP4 → receive file.  

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8+**  
- **Git**  
- **Virtualenv support** (`python3-venv`)  
- **FFmpeg** (for merging audio/video)  
- **A Telegram account**  

---

## 1. BotFather & Bot Token

1. Open Telegram and search for **@BotFather**.  
2. Send `/newbot` and follow prompts:
3. BotFather will reply with your **API token**.
4. Copy that token — you’ll need it in Step 2.

---

## 2. Local Setup

```bash
git clone https://github.com/hadibtf/TubeTap.git
cd TubeTap
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
.\.venv\Scripts\activate         # Windows PowerShell
pip install -r requirements.txt
```

Create `.env` file with:

```env
BOT_TOKEN=your_botfather_token_here
```

---

## 3. Cookie Authentication

Use the **Get cookies.txt** browser extension (Chrome or Brave), export, and save as `cookies.txt`.

---

## 4. Running Locally

```bash
python main.py
```

---

## 5. VPS Deployment Guide

### 5.1 System Installation (Ubuntu)

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip git ffmpeg -y
```

### 5.2 Install Google Chrome

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
```

### 5.3 Deploy & Run

```bash
cd ~
git clone https://github.com/hadibtf/TubeTap.git
cd TubeTap
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
nohup python main.py > bot.log 2>&1 &
```

---

## 6. Usage

1. Send YouTube link  
2. Bot asks format  
3. Choose MP3 or MP4  
4. Receive file  

---

## 7. Troubleshooting

- Install FFmpeg  
- Use correct `.env` format  
- Update cookies regularly  

---

## 8. Git Workflow & Contributing

```bash
git checkout dev
git checkout -b feature/your-feature-name
# code...
git add .
git commit -m "feat: your feature"
git push -u origin feature/your-feature-name
```

Then open a PR to `dev`.

---

## 9. License

MIT © TubeTap contributors  
