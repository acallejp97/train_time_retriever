import os
import subprocess
from telegram.ext import CommandHandler
from telegram.ext._application import Application

from utils import get_bot_token

async def ida(update, context):
    await update.message.reply_text('Buscando trenes de ida')
    subprocess.run(["python", "main.py", os.environ.get("ORIGIN"), os.environ.get("DESTINATION")])

async def vuelta(update, context):
    await update.message.reply_text('Buscando trenes de vuelta')
    subprocess.run(["python", "main.py", os.environ.get("DESTINATION"), os.environ.get("ORIGIN")])

async def start(update, context):
    await update.message.reply_text('Bot iniciado correctamente')

def main():
    token = get_bot_token()
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ida", ida))
    application.add_handler(CommandHandler("vuelta", vuelta))
    print("Listening...")
    application.run_polling(1.0)

main()