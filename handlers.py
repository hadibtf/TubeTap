from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from downloader import download_video, cleanup
import logging
import datetime
import os


# Use a Router for handler registration
router = Router()

class Download(StatesGroup):
    waiting_for_url = State()

@router.message(Command("start"))
async def start(message: types.Message):
    """Handles the /start command."""
    await message.reply("Hi! Send me a YouTube URL to download the video. Use /mp3 or /mp4 to specify the format.")

@router.message(Command("mp3"))
async def handle_mp3(message: types.Message, state: FSMContext):
    """Handles the /mp3 command."""
    await state.set_state(Download.waiting_for_url)
    await state.update_data(format='mp3')
    await message.reply("Please send me the YouTube URL.")

@router.message(Command("mp4"))
async def handle_mp4(message: types.Message, state: FSMContext):
    """Handles the /mp4 command."""
    await state.set_state(Download.waiting_for_url)
    await state.update_data(format='mp4')
    await message.reply("Please send me the YouTube URL.")

@router.message(Download.waiting_for_url, F.text)
async def process_url(message: types.Message, state: FSMContext):
    """Processes the YouTube URL."""
    data = await state.get_data()
    format_type = data.get('format', 'mp4')
    url = message.text

    # Clear state immediately
    await state.clear()

    try:
        sent_message = await message.reply("Downloading...")
        output_file, video_title = download_video(url, format_type)
        
        # Use FSInputFile to send local files
        input_file = types.FSInputFile(output_file)

        if format_type == 'mp3':
            await message.reply_audio(input_file, title=video_title)
        else:
            await message.reply_video(input_file, caption=video_title)
        
        await sent_message.delete()
        
        # Construct a log message
        log_message = (
            f"Timestamp: {datetime.datetime.now()}, "
            f"URL: {url}, "
            f"Format: {format_type}, "
            f"Size: {os.path.getsize(output_file)} bytes"
        )
        logging.info(log_message)
        
        # The original video file might have a different extension if yt-dlp chose a different format
        # Be robust in cleaning up
        base_filename, _ = os.path.splitext(output_file)
        cleanup(output_file, f"{base_filename}.mp4", f"{base_filename}.m4a", f"{base_filename}.webm")


    except ValueError as e:
        await message.reply(str(e))
    except Exception as e:
        logging.error(f"Error processing {url}: {e}")
        await message.reply("An error occurred while processing your request.")

