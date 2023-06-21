import instaloader
from instaloader import Profile
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_TELEGRAM_TOKEN' with your Telegram bot token
TOKEN = '5154547704:AAGpB62V1mpiXhCU0fiFk4S__WMTTlF6pPM'

# Create an instance of Instaloader
L = instaloader.Instaloader()

# Handle the '/start' command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to your Instagram bot!')

# Handle the '/inbox' command
def inbox(update: Update, context: CallbackContext) -> None:
    try:
        # Login to Instagram account
        L.login('your_username', 'your_password')

        # Get the authenticated user's profile
        profile = Profile.from_username(L.context, 'your_username')

        # Get the user's inbox
        inbox = profile.get_inbox()

        # Retrieve the last message
        last_message = inbox[0]

        # Send the last message to Telegram
        update.message.reply_text(f'Last Message:\n\n{last_message.text}')
    except instaloader.exceptions.LoginRequiredException:
        update.message.reply_text('Login required to access inbox.')
    except Exception as e:
        update.message.reply_text(f'An error occurred: {str(e)}')

# Handle incoming messages
def message_handler(update: Update, context: CallbackContext) -> None:
    try:
        # Login to Instagram account
        L.login('your_username', 'your_password')

        # Get the authenticated user's profile
        profile = Profile.from_username(L.context, 'your_username')

        # Get the user's inbox
        inbox = profile.get_inbox()

        # Retrieve the last message
        last_message = inbox[0]

        # Reply to the last message with the incoming Telegram message
        last_message.reply(context.bot, update.message.text)
    except instaloader.exceptions.LoginRequiredException:
        update.message.reply_text('Login required to send message.')
    except Exception as e:
        update.message.reply_text(f'An error occurred: {str(e)}')

# Handle the '/download' command
def download(update: Update, context: CallbackContext) -> None:
    try:
        shortcode = context.args[0]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target='downloads')
        update.message.reply_text('Post downloaded successfully!')
    except Exception as e:
        update.message.reply_text(f'An error occurred while downloading the post: {str(e)}')

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("inbox", inbox))
    dispatcher.add_handler(CommandHandler("download", download))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
