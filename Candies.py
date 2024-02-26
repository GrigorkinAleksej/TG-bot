from telegram import Update
from spy import*
from telegram.ext import CallbackContext
from handlers.player_profile import*

# Игра в конфеты в телеграм-боте
from random import randint

gd={}
gd['text1'] = 'сколько конфет возьмёте?'
BOT='Я, '

def game_type(update: Update, context: CallbackContext):
    log(update,context)
    play = update.message.text
    gd['player1']=update.effective_user.first_name+', '
    if play == '1': gd['player2']= BOT
    elif play == '2': gd['player2']= 'Игрок 2, '
    else:
        update.message.reply_text(f'До свидания')
        return ConversationHandler.END
    gd['player'] = gd['player1'] if randint(0, 1) else gd['player2']
    game()
    gd['text_msg']+=gd['text1']+'\n'
    update.message.reply_text(gd['text_msg'])
    gd['text_msg']=''
    return CANDY_ISDIGIT_STATE

def game():
    gd['text_msg']+=gd['player']
    if gd['player'] == BOT:
        gd['candies'] = gd['remains'] % (gd['priz']+1) if gd['remains'] % (gd['priz']+1) != 0 else randint(1, gd['priz'])
        gd['text_msg']+='взял '+str(gd['candies'])+' конфет\n'
        gd['text'] = ' Я ВЫИГРАЛ!'
        candy_remains()
        gd['player']=gd['player1']
    gd['candies'] = 0

def select_candy_isdigit(update: Update, context: CallbackContext):
# функция выбора количества конфет и проверки на число
    log(update,context)
    num = update.message.text
    text2 = 'Количество конфет должно быть натуральным числом\n'+gd['text1']
    while num == '0' or not num.isdigit():
        update.message.reply_text(text2)
        return CANDY_ISDIGIT_STATE
    gd['candies'] = int(num)
    if gd['candies'] < 1 or gd['candies'] > gd['priz']:
        gd['text_msg']+='Можно взять не более '+str(gd['priz'])+' конфет\n'
        update.message.reply_text(gd['text_msg'])
        gd['text_msg']=''
        return CANDY_ISDIGIT_STATE
    gd['text'] = ' ВЫ ВЫИГРАЛИ!'
    candy_remains()
    while gd['remains'] != 0:
        gd['player'] = gd['player2'] if gd['player'] == gd['player1'] else gd['player1']
        game()
        if gd['remains'] != 0:
            gd['text_msg']+=gd['text1']+'\n'
            update.message.reply_text(gd['text_msg'])
            gd['text_msg']=''
            return CANDY_ISDIGIT_STATE
    gd['text_msg']+='\n'+gd['player']+gd['text']+'\nПродолжим?'
    update.message.reply_text(gd['text_msg'])
    return GAME_CANDIES_STATE

def candy_remains():
# Сообщение об остатках конфет
    gd['remains'] = 0 if gd['remains'] < gd['candies'] else gd['remains'] - gd['candies']
    gd['text_msg']+=f"Осталось конфет: {gd['remains']}\n"

def game_candies(update: Update, context: CallbackContext):
    log(update,context)
    gd['remains'] = randint(180, 280)
    gd['priz'] = randint(18, 38)
    update.message.reply_text(f'ИГРА\nНа столе лежит {gd["remains"]} конфет.\n'
        f'Играют два игрока делая ход друг после друга.\n'
        f'Первый ход определяется жеребьёвкой.\n'
        f'За один ход можно забрать не более чем {gd["priz"]} конфет.\n'
        f'Пропускать ход нельзя.\n'
        f'Все конфеты оппонента достаются сделавшему последний ход.\n'
        f'1 - игра с компьютером\n2 - игра двух людей\nдругое - отказ от игры\n'
        f'Выберите тип игры: ')
    gd['text_msg']=''
    return GAME_TYPE_STATE