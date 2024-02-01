import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
TUNNEL_URL = 'https://yoursubdomain.ngrok.io'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a command to execute!')

def execute_command(update: Update, context: CallbackContext) -> None:
    command = update.message.text[5:]
    response = requests.post(f'{TUNNEL_URL}/command', json={'command': command})

    if response.status_code == 200:
        update.message.reply_text(response.json()['output'])
    else:
        update.message.reply_text('Error executing command.')

def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('cmd', execute_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
