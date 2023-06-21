import os
import logging
import instaloader
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import ParseMode, Update

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Get your Telegram bot token from environment variable
TOKEN = os.environ.get('6241362530:AAHq-3ruJbiYbVRZoT4rAx8hSMGy5tGksq4')

# Initialize Instaloader
loader = instaloader.Instaloader()

def start(update: Update, context: CallbackContext):
    """Handler for the /start command."""
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Welcome! Just send me the link to an Instagram Reel or post and I will provide you with the download link.")

def download_instagram_post(update: Update, context: CallbackContext):
    """Handler for downloading Instagram posts."""
    instagram_post = update.message.text

    try:
        # Download the post using Instaloader
        shortcode = instaloader.utils.get_shortcode_from_url(instagram_post)
        loader.download_by_shortcode(shortcode, target=f"{shortcode}")
        file_path = f"{shortcode}/{shortcode}.jpg"
        
        # Send the downloaded post as a photo
        context.bot.send_photo(chat_id=update.message.chat_id,
                               photo=open(file_path, 'rb'))
    except Exception as e:
        logging.error(f"Error downloading Instagram post: {e}")
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, I couldn't download the Instagram post.")

def download_instagram_reel(update: Update, context: CallbackContext):
    """Handler for downloading Instagram Reels."""
    instagram_reel = update.message.text

    try:
        # Send the Instagram Reel URL as a message
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=f"Here is the link to the Instagram Reel: {instagram_reel}")
    except Exception as e:
        logging.error(f"Error sending Instagram Reel link: {e}")
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text="Sorry, I couldn't send the Instagram Reel link.")

def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(CommandHandler("start", start))

    # Add message handlers
    dp.add_handler(MessageHandler(Filters.regex(r'https?://(www\.)?instagram\.com/.*'), download_instagram_post))
    dp.add_handler(MessageHandler(Filters.regex(r'https?://(www\.)?instagram\.com/reel/.*'), download_instagram_reel))

    # Start the bot
    updater.start_polling()
    logging.info("Bot started!")
    updater.idle()

if __name__ == '__main__':
    main()
  
