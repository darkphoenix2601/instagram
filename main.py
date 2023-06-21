from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram import Update, ParseMode
from instagram_private_api import Client
import logging
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.StreamHandler()])

TOKEN = "6241362530:AAGABEK3ngb5Lg1sQF1KbPHK29FSkWEgyUs"

def download_insta_post(media_url: str):
    try:
        session = requests.Session()
        session.headers.update({"User-Agent": "Mozilla/5.0"})

        api = Client()

        post_id = media_url.split("/")[-2]
        media_info = api.media_info(post_id)
        media_url = media_info.get("video_url") or media_info.get("photo_url")

        if media_url:
            response = session.get(media_url)
            if response.status_code == 200:
                filename = post_id + ".mp4" if media_info.get("video_url") else post_id + ".jpg"
                with open(filename, "wb") as f:
                    f.write(response.content)
                return filename

    except Exception as e:
        logging.error(f"Error downloading Instagram post: {e}")

    return None


def download(update: Update, context: CallbackContext):
    message = update.effective_message
    instagram_post = message.text

    if instagram_post == "/start":
        context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        update.message.reply_text(
            "❤️ Thanks For Using Me Just Send Me the Link in the Following Format:\n"
            "🔥 Format: https://www.instagram.com/p/B4zvXCIlNTw/\n"
            "Videos Must Be Less Than 20MB, and it Supports Public and Private Posts\n"
            "\n<b>🌀 Source:</b> [GitHub](https://github.com/darkphoenix2601/instagram)",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    else:
        filename = download_insta_post(instagram_post)
        if filename:
            with open(filename, "rb") as f:
                if filename.endswith(".mp4"):
                    context.bot.send_video(chat_id=update.message.chat_id, video=f)
                else:
                    context.bot.send_photo(chat_id=update.message.chat_id, photo=f)
        else:
            context.bot.sendMessage(chat_id=update.message.chat_id, text="Invalid Instagram URL")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    logging.info("Setting Up MessageHandler")
    dp.add_handler(MessageHandler(Filters.text, download))
    updater.start_polling()
    logging.info("Bot started!")
    updater.idle()

if __name__ == "__main__":
    main()
  
