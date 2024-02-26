from telegram import Update
from spy import*
from telegram.ext import CallbackContext
from handlers.player_profile import*

# Игра в ""Крестики-нолики"".
import random

gd={}
BOT='Я, '

def set_pole(znak, cell):
    # изменение состояния поля и проверка на победу
    i=(cell-1)//3
    j=(cell-1)%3
    gd['pole'][i][j] = znak
    gd['line'][i] = gd['line'][i].replace(str(cell), znak)
    strike = 0
    for k in range(3):
        if gd['pole'][i][k] == znak: strike += 1
    if strike == 3: return True
    strike = 0
    for k in range(3):
        if gd['pole'][k][j] == znak: strike += 1
    if strike == 3: return True
    strike = 0
    if i == j:
        for k in range(3):
            if gd['pole'][k][k] == znak: strike += 1
        if strike == 3: return True
    strike = 0
    if i+j == 2:
        for k in range(3):
            if gd['pole'][k][2-k] == znak: strike += 1
        if strike == 3: return True
    return False

def intellect_bot(player):
    # Логика бота по выбору номера клетки
    for z in [player[1], player[2]]:
        for i in range(3):
            for j in range(3):
                if gd['pole'][i][j] == '':
                    k = j+1
                    if k == 3: k = 0
                    if gd['pole'][i][k] == z:
                        l = k+1
                        if l == 3: l = 0
                        if gd['pole'][i][l] == gd['pole'][i][k]: return i*3+j+1
                    k = i+1
                    if k == 3: k = 0
                    if gd['pole'][k][j] == z:
                        l = k+1
                        if l == 3: l = 0
                        if gd['pole'][l][j] == gd['pole'][k][j]: return i*3+j+1
                    if i == j:
                        k = i+1
                        if k == 3: k = 0
                        if gd['pole'][k][k] == z:
                            l = k+1
                            if l == 3: l = 0
                            if gd['pole'][l][l] == gd['pole'][k][k]: return i*3+j+1
                    if i+j == 2:
                        k = i+1
                        if k == 3: k = 0
                        if gd['pole'][k][2-k] == z:
                            l = k+1
                            if l == 3: l = 0
                            if gd['pole'][l][2-l] == gd['pole'][k][2-k]: return i*3+j+1
    if gd['pole'][1][1] == '': return 5
    for i in range(3):
        for j in range(3):
            if gd['pole'][i][j] == '':
                k = j+1
                if k == 3: k = 0
                if gd['pole'][i][k] == player[2]: continue
                l = k+1
                if l == 3: l = 0
                if gd['pole'][i][l] == player[2]: continue
                k = i+1
                if k == 3: k = 0
                if gd['pole'][k][j] == player[2]: continue
                l = k+1
                if l == 3: l = 0
                if gd['pole'][l][j] == player[2]: continue
                if i == j:
                    k = i+1
                    if k == 3: k = 0
                    if gd['pole'][k][k] == player[2]: continue
                    l = k+1
                    if l == 3: l = 0
                    if gd['pole'][l][l] == player[2]: continue
                if i+j == 2:
                    k = i+1
                    if k == 3: k = 0
                    if gd['pole'][k][2-k] == player[2]: continue
                    l = k+1
                    if l == 3: l = 0
                    if gd['pole'][l][2-l] == player[2]: continue
                    return i*3+j+1
    number=0
    while number==0:
        if gd['pole'][0][1] != '' and gd['pole'][1][0] != '' and gd['pole'][1][2] != '' and gd['pole'][2][1] != '':
            number = random.randint(1, 9)
        elif gd['pole'][0][0] != '' and gd['pole'][0][2] != '' and gd['pole'][2][2] != '' and gd['pole'][2][0] != '':
            number = random.randint(2, 8)
        elif gd['pole'][1][1] == player[2]:
            number = 2
            while not number % 2: number = random.randint(1, 9)
        else:
            number = 1
            while number % 2: number = random.randint(2, 8)
        if gd['pole'][(number-1)//3][(number-1) % 3] != '': number=0
    return number

def not_winner():
# Проверка заполненности поля и смена игрока, делающего ход
    finish = True
    for i in range(3):
        for j in range(3):
            if gd['pole'][i][j] == '': finish = False
    if finish:
        gd['text_msg']+='НИЧЬЯ\nПовторим?'
        return GAME_CROSSES_STATE
    if gd['first'] == 1:
        gd['player'] = gd['player1']
        gd['first'] = 2
    else:
        gd['player'] = gd['player2']
        gd['first'] = 1
    return -1

def bot_hod():
# Ход бота
    cell = intellect_bot(gd['player2'])
    winner = set_pole(gd['player2'][1], cell)
    gd['game_pole']=f"\n{gd['line'][0]}{gd['gs']}{gd['line'][1]}{gd['gs']}{gd['line'][2]}\n"
    gd['text_msg']+=f'Я выбираю {cell}\n'+gd['game_pole']
    if winner:
        gd['text_msg']+=' Я ВЫИГРАЛ!\nПовторим?'
        return GAME_CROSSES_STATE
    if not_winner()==GAME_CROSSES_STATE: return GAME_CROSSES_STATE
    return -1

def game_crosses(update: Update, context: CallbackContext):
    log(update,context)
    update.message.reply_text(f'ИГРА\nКрестики-нолики\n\n1 - игра с компьютером\n'
        f'2 - игра двух людей\nдругое - отказ от игры\nВыберите тип игры: ')
    gd['text_msg']=''
    return GAME_CROSSES_TYPE_STATE

def game_crosses_type(update: Update, context: CallbackContext):
    log(update,context)
    play = update.message.text
    gd['player1']=[update.effective_user.first_name+', ','','']
    if play == '1': gd['player2']= [BOT, '', '']
    elif play == '2': gd['player2']= ['Игрок 2, ', '', '']
    else:
        update.message.reply_text(f'До свидания')
        return ConversationHandler.END
    # Переключение между игроками
    gd['line'] = ['  1   |  2  |  3', '  4  |  5  |  6', '  7  |  8  |  9']
    gd['pole'] = [['', '', ''], ['', '', ''], ['', '', '']]
    gd['player']=['','','']
    gd['first'] = random.randint(1, 2)
    if gd['first'] == 1:
        gd['player1'][1] = 'X'
        gd['player1'][2] = 'O'
        gd['player2'][1] = 'O'
        gd['player2'][2] = 'X'
    else:
        gd['player1'][1] = 'O'
        gd['player1'][2] = 'X'
        gd['player2'][1] = 'X'
        gd['player2'][2] = 'O'
    not_winner()
    gd['gs']='\n___|___|___\n'
    gd['game_pole']=f"\n{gd['line'][0]}{gd['gs']}{gd['line'][1]}{gd['gs']}{gd['line'][2]}\n"
    gd['text_msg']=gd['game_pole']
    if gd['player'][0] == BOT:
        bot_hod()
    # Запрос номера клетки
    gd['text_msg']+=gd['player'][0]+'\nКуда сделать ход?\n'
    update.message.reply_text(gd['text_msg'])
    gd['text_msg']=''
    return INPUT_CELL_STATE

def input_cell(update: Update, context: CallbackContext):
    # Ввод номера клетки
    log(update,context)
    cell = update.message.text
    while not cell.isdigit() or cell=='0':
        update.message.reply_text(f'Номер клетки должен быть натуральным числом\nКуда сделать ход?\n')
        return INPUT_CELL_STATE
    cell=int(cell)
    if cell > 9:
        update.message.reply_text('Клеток всего 9')
        return INPUT_CELL_STATE
    if gd['pole'][(cell-1)//3][(cell-1) % 3] != '':
        update.message.reply_text('Это поле уже занято')
        return INPUT_CELL_STATE
    winner = set_pole(gd['player'][1], cell)
    gd['game_pole']=f"\n{gd['line'][0]}{gd['gs']}{gd['line'][1]}{gd['gs']}{gd['line'][2]}\n"
    gd['text_msg']=gd['game_pole']
    if winner:
        gd['text_msg']+=gd['player'][0]+' ВЫ ВЫИГРАЛИ!\nПовторим?'
        update.message.reply_text(gd['text_msg'])
        return GAME_CROSSES_STATE
    if not_winner()==GAME_CROSSES_STATE:
        update.message.reply_text(gd['text_msg'])
        return GAME_CROSSES_STATE
    if gd['player'][0] == BOT:
        if bot_hod()==GAME_CROSSES_STATE:
            update.message.reply_text(gd['text_msg'])
            return GAME_CROSSES_STATE
    gd['text_msg']+=gd['player'][0]+'Куда сделать ход?\n'
    update.message.reply_text(gd['text_msg'])
    gd['text_msg']=''
    return INPUT_CELL_STATE
