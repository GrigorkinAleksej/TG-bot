from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

user_profile = {}
(
    PLAYER_NAME_STATE,  # 0
    PLAYER_AGE_STATE,  # 1
    PLAYER_GENDER_STATE,  # 2
    GAME_CANDIES_STATE,  # 3
    GAME_TYPE_STATE,
    CANDY_ISDIGIT_STATE,
    GAME_CROSSES_STATE,
    GAME_CROSSES_TYPE_STATE,
    INPUT_CELL_STATE,
) = range(9)

def input_player_name_handler(update: Update, context: CallbackContext) -> int:
    name = update.message.text
    user_profile["name"] = name
    update.message.reply_text(f"Введите возраст:")
    return PLAYER_AGE_STATE

def input_player_age_handler(update: Update, context: CallbackContext) -> int:
    age = update.message.text
    if not age.isdigit():
        update.message.reply_text(f"Ошибка! Введите возраст число: ")
        return PLAYER_AGE_STATE
    user_profile["age"] = int(age)
    reply_kb_markup = ReplyKeyboardMarkup([ ["М", "Ж"], ], one_time_keyboard=True)
    update.message.reply_text(f"Введите пол:", reply_markup=reply_kb_markup)
    return PLAYER_GENDER_STATE

def input_player_gender_handler(update: Update, context: CallbackContext) -> int:
    user_profile["gender"] = update.message.text
    update.message.reply_text(f"Вы ввели следующую информацию: {user_profile}")
    return ConversationHandler.END