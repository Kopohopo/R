from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import Unauthorized

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '6887337730:AAHizbsBEqara95OzVvAVGLvvjiPoyoYZlQ'

# Chat ID of the user to forward deleted messages
FORWARD_CHAT_ID = '6679011306,1509696612'

def start(update: Update, context: CallbackContext) -> None:
    if update.message:
        update.message.reply_text('Bot is running!')

def check_message(update: Update, context: CallbackContext) -> None:
    # Check if the message has been edited
    if update.edited_message:
        # Get the edited message
        edited_message = update.edited_message
        # Get the name of the user who edited the message
        edited_by_user = edited_message.from_user.username or edited_message.from_user.first_name
        # Forward the deleted message to the specified user
        forward_message_text = f"Message edited by {edited_by_user}"
        try:
            if update.message and update.message.chat_id:
                forward_message_text += f" in group {update.message.chat_id}"
            forward_message_text += f":\n{edited_message.text}"
            # Send the message to '@kirahume'
            context.bot.send_message(chat_id=FORWARD_CHAT_ID, text=forward_message_text)
            # Delete the edited message
            edited_message.delete()
        except Unauthorized:
            print(f"Unauthorized: Could not forward message to {FORWARD_CHAT_ID}")


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.all & (~Filters.command), check_message))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
