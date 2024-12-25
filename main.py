from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests


from config import API_ID, API_HASH, BOT_TOKEN, API_KEY, BASE_URL, SUPPORT_LINK, UPDATES_LINK, BOT_USERNAME


app = Client("message_handler_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start_command(bot, message):
    try:
        await message.reply_photo(
                            photo = f"https://files.catbox.moe/6bym0w.jpg",
                            caption = f"Hey,\n\nWelcome to HEAL AI BOT\n\n This is your ai doctor which can predict your disease through your symptoms and gives cure remedies!\n\nPlease tell me about your disease or symptoms so I can help you.",
            
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
                    f"{result}",
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
