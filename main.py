from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode, Update
import logging
import requests
import json
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.StreamHandler()])

TOKEN = "6241362530:AAErqsOBc0BF8H1O7dJyHd_LKaWvFnpHcu8"

def download(update: Update, context: CallbackContext):
    message = update.effective_message
    instagram_post = message.text
    if instagram_post == "/start":
        context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        update.message.reply_text("❤️ Thanks For Using Me Just Send Me The Link In Below Format  \n🔥 Format :- https://www.instagram.com/p/B4zvXCIlNTw/ \nVideos Must Be Less Than 20MB, For Now, It Cannot Support Long IGTV Videos \n\n<b>Support Group :-</b> @Technology_Arena \n<b>🌀 Source</b> \nhttps://github.com/TheDarkW3b/instagram", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        pass

    if "instagram.com" in instagram_post:
        shortcode_match = re.search(r"/([A-Za-z0-9_-]{11})/", instagram_post)
        if shortcode_match:
            shortcode = shortcode_match.group(1)
            url = f"https://instagram.com/p/{shortcode}?__a=1"
            try:
                visit = requests.get(url).json()
            except:
                context.bot.sendMessage(chat_id=update.message.chat_id, text="Invalid Instagram URL")
                return

            if "graphql" in visit:
                media_info = visit["graphql"]["shortcode_media"]
                is_video = media_info.get("is_video", False)

                if is_video:
                    video_url = media_info.get("video_url")
                    if video_url:
                        context.bot.send_chat_action(chat_id=update.message.chat_id, action="upload_video")
                        context.bot.send_video(chat_id=update.message.chat_id, video=video_url)
                    else:
                        context.bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, unable to download the video.")
                else:
                    photo_url = media_info.get("display_url")
                    if photo_url:
                        context.bot.send_chat_action(chat_id=update.message.chat_id, action="upload_photo")
                        context.bot.send_photo(chat_id=update.message.chat_id, photo=photo_url)
                    else:
                        context.bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, unable to download the photo.")
            else:
                context.bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, unsupported Instagram URL.")
        else:
            context.bot.sendMessage(chat_id=update.message.chat_id, text="Invalid Instagram URL")
    else:
        context.bot.sendMessage(chat_id=update.message.chat_id, text="Kindly Send Me Public Instagram Video/Photo URL")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    logging.info("Setting Up MessageHandler")
    dp.add_handler(MessageHandler(Filters.text, download))
    updater.start_polling()
    logging.info("Starting Long Polling!")
    updater.idle()


if __name__ == "__main__":
    main()
      
