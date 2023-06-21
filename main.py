from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode, Update
import logging
import instaloader

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    handlers=[logging.StreamHandler()])

TOKEN = "5154547704:AAHQcQ6s6Q6Pp489eWQ2pL2keZle7-Us7TM"
USERNAME = "gods.myth"
PASSWORD = "kartik@2601"

def download(update: Update, context: CallbackContext):
    message = update.effective_message
    instagram_post = message.text
    if instagram_post == "/start":
        context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
        update.message.reply_text("❤️ Thanks For Using Me Just Send Me The Link In Below Format  \n🔥 Format :- https://www.instagram.com/p/B4zvXCIlNTw/ \nVideos Must Be Less Than 20MB, For Now, It Cannot Support Long IGTV Videos \n\n<b>Support Group :-</b> @Technology_Arena \n<b>🌀 Source</b> \nhttps://github.com/TheDarkW3b/instagram", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    else:
        pass

    if "instagram.com" in instagram_post:
        try:
            loader = instaloader.Instaloader()
            loader.login(USERNAME, PASSWORD)
            post_url = instagram_post.strip().split("?")[0]
            loader.download_post(post_url, target=".")
            context.bot.send_chat_action(chat_id=update.message.chat_id, action="upload_photo")
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open(f"{post_url}.jpg", "rb"))
        except Exception as e:
            logging.error(f"Error downloading Instagram post: {e}")
            context.bot.sendMessage(chat_id=update.message.chat_id, text="Error downloading Instagram post.")
    else:
        context.bot.sendMessage(chat_id=update.message.chat_id, text="Kindly Send Me Public Instagram Post URL")


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
  
