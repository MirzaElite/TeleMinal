import os
import paramiko
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set up the SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Replace these variables with your own values
LINUX_HOST = "your_linux_host"
LINUX_USER = "your_linux_user"
LINUX_PASSWORD = "your_linux_password"

# Connect to the Linux machine
try:
    ssh.connect(LINUX_HOST, username=LINUX_USER, password=LINUX_PASSWORD)
except Exception as e:
    print(f"Failed to connect to Linux machine: {e}")
    exit(1)

# Define the Telegram bot command handler
def handle_command(update: Update, context: CallbackContext) -> None:
    command = update.message.text[len("/"):]
    stdin, stdout, stderr = ssh.exec_command(command)

    # Print the output to the console
    for line in stdout:
        print(line.strip())

    # Send the output back to the Telegram group
    context.bot.send_message(chat_id=update.effective_chat.id, text=stdout.read().decode())

def main() -> None:
    # Replace TOKEN with your Telegram bot token
    updater = Updater(token="TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("run", handle_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
