from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from downloader import download_mp3, download_mp4, cleanup
from states import Conversation
import logging
import re

# Use a Router for handler registration
router = Router()

# Regex to validate YouTube URLs
YOUTUBE_URL_REGEX = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'

@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    """Handles the /start command and sets the state to wait for a link."""
    await state.set_state(Conversation.WAITING_FOR_LINK)
    await message.reply("🎬 Send me a YouTube link to download!")

@router.message(Conversation.WAITING_FOR_LINK, F.text)
async def handle_link(message: types.Message, state: FSMContext):
    """Handles receiving the YouTube link."""
    if not re.match(YOUTUBE_URL_REGEX, message.text):
        await message.reply("That doesn't look like a valid YouTube link. Please try again.")
        return

    await state.update_data(url=message.text)
    await state.set_state(Conversation.WAITING_FOR_FORMAT)

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="MP3")],
            [types.KeyboardButton(text="MP4")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.reply("Choose the format:", reply_markup=keyboard)

@router.message(Conversation.WAITING_FOR_FORMAT, F.text == "MP3")
async def handle_mp3_selection(message: types.Message, state: FSMContext):
    """Handles the MP3 format selection."""
    data = await state.get_data()
    url = data.get("url")
    await state.clear()
    
    # Remove the keyboard
    await message.reply("Downloading MP3...", reply_markup=types.ReplyKeyboardRemove())

    try:
        sent_message = await message.answer("Processing...")
        output_file, video_title = download_mp3(url)
        
        input_file = types.FSInputFile(output_file)
        await message.reply_audio(input_file, title=video_title)
        
        await sent_message.delete()
        cleanup(output_file)

    except ValueError as e:
        await message.reply(str(e))
    except Exception as e:
        logging.error(f"Error processing {url} for MP3: {e}")
        await message.reply("An error occurred while processing your request.")
    finally:
        await state.clear()


@router.message(Conversation.WAITING_FOR_FORMAT, F.text == "MP4")
async def handle_mp4_selection(message: types.Message, state: FSMContext):
    """Handles the MP4 format selection."""
    data = await state.get_data()
    url = data.get("url")
    await state.clear()

    # Remove the keyboard
    await message.reply("Downloading MP4...", reply_markup=types.ReplyKeyboardRemove())

    try:
        sent_message = await message.answer("Processing...")
        output_file, video_title = download_mp4(url)
        
        input_file = types.FSInputFile(output_file)
        await message.reply_video(input_file, caption=video_title)
        
        await sent_message.delete()
        cleanup(output_file)

    except ValueError as e:
        await message.reply(str(e))
    except Exception as e:
        logging.error(f"Error processing {url} for MP4: {e}")
        await message.reply("An error occurred while processing your request.")
    finally:
        await state.clear()

@router.message(Conversation.WAITING_FOR_FORMAT)
async def handle_invalid_format_selection(message: types.Message):
    """Handles invalid selections when waiting for a format."""
    await message.reply("Invalid selection. Please choose either MP3 or MP4 from the keyboard.")