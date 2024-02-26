from telegram import Update
from telegram.ext import CallbackContext
import datetime

def log(update: Update, context: CallbackContext):
    file=open('db.csv','a', encoding='utf-8')
    file.write(f'{datetime.datetime.now().date()},{datetime.datetime.now().time()},{update.effective_user.first_name},{update.effective_user.id},{update.message.text}\n')
    file.close()

