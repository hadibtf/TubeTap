from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher
from downloader import download_video, cleanup
import logging
import datetime

class Download(StatesGroup):
    waiting_for_url = State()

async def start(message: types.Message):
    """Handles the /start command."""
    await message.reply("Hi! Send me a YouTube URL to download the video. Use /mp3 or /mp4 to specify the format.")

async def handle_mp3(message: types.Message, state: FSMContext):
    """Handles the /mp3 command."""
    await state.update_data(format='mp3')
    await Download.waiting_for_url.set()
    await message.reply("Please send me the YouTube URL.")

async def handle_mp4(message: types.Message, state: FSMContext):
    """Handles the /mp4 command."""
    await state.update_data(format='mp4')
    await Download.waiting_for_url.set()
    await message.reply("Please send me the YouTube URL.")

async def process_url(message: types.Message, state: FSMContext):
    """Processes the YouTube URL."""
    data = await state.get_data()
    format = data.get('format', 'mp4')
    url = message.text

    try:
        sent_message = await message.reply("Downloading...")
        output_file, video_title = download_video(url, format)
        
        with open(output_file, 'rb') as file:
            if format == 'mp3':
                await message.reply_audio(file, title=video_title)
            else:
                await message.reply_video(file, caption=video_title)
        
        await sent_message.delete()
        
        logging.info(f"{datetime.datetime.now()} - {url} - {video_title}")
        
        cleanup(output_file, f"{output_file.split('.')[0]}.mp4")

    except ValueError as e:
        await message.reply(str(e))
    except Exception as e:
        logging.error(f"Error processing {url}: {e}")
        await message.reply("An error occurred while processing your request.")
    finally:
        await state.finish()

def register_handlers(dp: Dispatcher):
    """Registers the message handlers."""
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(handle_mp3, commands=['mp3'])
    dp.register_message_handler(handle_mp4, commands=['mp4'])
    dp.register_message_handler(process_url, state=Download.waiting_for_url)
