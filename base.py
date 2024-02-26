from telegram import Update
from telegram.ext import CallbackContext
from spy import*
from handlers.player_profile import PLAYER_NAME_STATE

SPISOK1='Список команд:\n /player_profile - опрос\n /candies - игра в конфеты\n /crosses - игра в крестики-нолики\n'
SPISOK2='/hi - привет\n/time - текущее время\n/sum - sum a b - сумма двух чисел\n/help - список команд\n'
SPISOK=SPISOK1+SPISOK2

def start(update: Update, context: CallbackContext) -> None:
# Отправить сообщение, когда будет выдана команда /Start
    log(update,context)
    user = update.effective_user
    update.message.reply_text(f'Привет {user.first_name}!\n {SPISOK}')

def player_profile_command(update: Update, context: CallbackContext) -> int:
    log(update,context)
    update.message.reply_text(f"Введите имя: ")
    return PLAYER_NAME_STATE

def hi_command(update: Update, context: CallbackContext):
    log(update,context)
    update.message.reply_text(f'Привет, {update.effective_user.first_name},!')

def help_command(update: Update, context: CallbackContext):
    log(update,context)
    update.message.reply_text(SPISOK)

def time_command(update: Update, context: CallbackContext):
    log(update,context)
    update.message.reply_text(f'{datetime.datetime.now().time()}')

def sum_command(update: Update, context: CallbackContext):
    log(update,context)
    msg=update.message.text
    print(msg)
    item=msg.split()
    x=int(item[1])
    y=int(item[2])
    update.message.reply_text(f'{x}+{y}={x+y}')