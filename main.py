from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
import requests
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = "YOUR_API_ID"  
API_HASH = "YOUR_API_HASH"  
BOT_TOKEN = "YOUR_BOT_TOKEN"  


API_KEY = "YOUR_API_KEY"  
BASE_URL = "https://api.openai.com/v1/chat/completions"

app = Client("baby_ai_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)



@app.on_message(filters.command("start"))
async def start_command(bot, message):
    try:

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("➕ Add Me to Your Group", url="https://t.me/YOUR_BOT_USERNAME?startgroup=true"),
                ],
                [
                    InlineKeyboardButton("👥 Support", url="https://t.me/BABY09_WORLD"),
                    InlineKeyboardButton("📢 Updates", url="https://t.me/BABY09_UPDATES"),
                ],
            ]
        )

        
        await message.reply_text(
            "👋 **Welcome to AI Bot!**\n\n"
            "I can answer your queries and assist you. Just type your message to get started.\n\n"
            "Use me wisely and have fun!\n\n"
            "🔹 Maintained by [Baby-Music](https://t.me/BABY09_WORLD)",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        print(f"Error in /start command: {e}")
        await message.reply_text("❍ ᴇʀʀᴏʀ: Unable to process the command.")




@app.on_message(filters.text)
async def handle_messages(bot, message):
    try:
        
        unwanted_symbols = ["/", ":", ";", "*", "?"]

        
        if message.text[0] in unwanted_symbols:
            print(f"Ignored message: {message.text}")  
            return  

        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        query = message.text
        print(f"Processing query: {query}")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)

        if response.status_code == 200 and response.text.strip():
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                result = response_data["choices"][0]["message"]["content"]
                await message.reply_text(
                    f"{result} \n\nＡɴsᴡᴇʀᴇᴅ ʙʏ➛[˹ ʙᴀʙʏ-ᴍᴜsɪᴄ ™˼𓅂](https://t.me/BABY09_WORLD)",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await message.reply_text("❍ ᴇʀʀᴏʀ: No response from API.")
        else:
            await message.reply_text(f"❍ ᴇʀʀᴏʀ: API request failed. Status code: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")
        await message.reply_text(f"❍ ᴇʀʀᴏʀ: {e}")



if __name__ == "__main__":
    print("Bot is running...")
    app.run()
