from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode, Update
import logging
import instaloader

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.StreamHandler()])

TOKEN = "6241362530:AAHq-3ruJbiYbVRZoT4rAx8hSMGy5tGksq4"

def download(update: Update, context: CallbackContext):
    message = update.effective_message
    instagram_post = message.text
    if instagram_post == "/start":
        context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        update.message.reply_text("❤️ Thanks For Using Me Just Send Me The Link In Below Format  \n🔥 Format :- https://www.instagram.com/p/B4zvXCIlNTw/ \nVideos Must Be Less Than 20MB, For Now, It Cannot Support Long IGTV Videos \n\n<b>Support Group :-</b> @Technology_Arena \n<b>🌀 Source</b> \nhttps://github.com/TheDarkW3b/instagram", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        pass

    if "instagram.com" in instagram_post:
        loader = instaloader.Instaloader()
        try:
            shortcode = instaloader.utils.get_shortcode_from_url(instagram_post)
            loader.download_by_shortcode(shortcode, target="#tmp")
            file_path = f"#tmp/{shortcode}.mp4"
            context.bot.send_chat_action(chat_id=update.message.chat_id, action="upload_video")
            context.bot.send_video(chat_id=update.message.chat_id, video=open(file_path, 'rb'))
        except:
            context.bot.sendMessage(chat_id=update.message.chat_id, text="Invalid Instagram URL")
    else:
        context.bot.sendMessage(chat_id=update.message.chat_id, text="Kindly Send Me Public Instagram Reels URL")


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
