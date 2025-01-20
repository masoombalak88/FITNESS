from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import requests
from gtts import gTTS
import os
from config import API_ID, API_HASH, BOT_TOKEN

API_ID = '12380656'  # Replace with your API ID
API_HASH = 'd927c13beaaf5110f25c505b7c071273'  # Replace with your API Hash
BOT_TOKEN = '7757056868:AAF0vnPl-xaX8JM8IQ7qO2-Wn0JfuxSCsqY'  # Replace with your Bot Token

# Initialize the bot client
app = Client("message_handler_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store replies temporarily based on message IDs
message_responses = {}

# Function to convert text to speech and send it as an audio file
def text_to_speech(text, chat_id):
    tts = gTTS(text=text, lang='en')
    file_path = 'audio.mp3'
    tts.save(file_path)
    
    # Send the audio file to the user
    app.send_audio(chat_id=chat_id, audio=file_path)
    os.remove(file_path)  # Clean up the temporary audio file

# Handler for the /start command
@app.on_message(filters.command("start"))
async def start_command(bot, message):
    try:
        await message.reply_photo(
            photo="https://files.catbox.moe/ske2d0.jpg",
            caption=(
                "🌟 🌟 Welcome to Healix AI Fitness Bot – Your Ultimate Fitness Companion! 🌟\n\n👨‍⚕️ What Can I Help With?\n"
                "🔹 Guide you through beginner fitness steps.\n"
                "🔹 Answer all your fitness-related questions.\n🔹 Create personalized daily fitness goals and diet plans.\n\n"
                "✨ How Does It Work?\n✅ It’s simple! Share your fitness needs, and I’ll deliver AI-driven insights tailored just for you—instantly and effortlessly.\n\n"
                "💪 Let’s elevate your fitness journey together—smarter, faster, and better! 💖"

            ),
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        print(f"Error in /start command: {e}")
        await message.reply_text("❍ ᴇʀʀᴏʀ: Unable to process the command.")

# Handler for the /doctor command (group)
@app.on_message(filters.command("doctor") & filters.group)
async def fetch_med_info(client, message):
    query = " ".join(message.command[1:])  # Extract the query after the command
    if not query:
        await message.reply_text("Please provide a medical query to ask.")
        return

    # Send typing action to indicate bot is working
    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Use the API to get medical data
    api_url = f"https://fitness.codesearch.workers.dev/?chat={query}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            reply = data.get("data", "Sorry, I couldn't fetch the data.")
        else:
            reply = "Failed to fetch data from the API."
    except Exception as e:
        reply = f"An error occurred: {e}"

    # Store the response text for later use
    message_responses[message.id] = reply

    # Add TTS inline button to reply
    await message.reply_text(
        reply,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Convert to TTS", callback_data=f'tts_{message.id}')]
        ])
    )

# Handler for private message queries (DM/PM), ignoring commands
@app.on_message(filters.private & ~filters.command(["start", "doctor"]))
async def handle_private_query(client, message):
    query = message.text.strip()  # Use the message text as the query
    if not query:
        await message.reply_text("Please provide a medical query.")  # Inform the user if no query is provided
        return

    # Send typing action to indicate bot is working
    await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

    # Use the API to get medical data
    api_url = f"https://fitness.codesearch.workers.dev/?chat={query}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            reply = data.get("data", "Sorry, I couldn't fetch the data.")
        else:
            reply = "Failed to fetch data from the API."
    except Exception as e:
        reply = f"An error occurred: {e}"

    # Store the response text for later use
    message_responses[message.id] = reply

    # Add TTS inline button to reply
    await message.reply_text(
        reply,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Convert to TTS", callback_data=f'tts_{message.id}')]
        ])
    )

# Handler for button click (Convert to TTS)
@app.on_callback_query(filters.regex('^tts_'))
def on_button_click(client, callback_query):
    # Extract the message ID from callback data
    message_id = int(callback_query.data.split('_')[1])

    # Retrieve the response text from stored data
    text = message_responses.get(message_id, "No data found.")

    # Send the TTS version of the message
    text_to_speech(text, callback_query.message.chat.id)

    # Acknowledge the button click
    callback_query.answer()

    # Optionally remove the entry from the dictionary after processing
    del message_responses[message_id]

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
