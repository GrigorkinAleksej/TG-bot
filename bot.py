import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from commands.base import start, player_profile_command, hi_command, time_command, help_command, sum_command
from handlers.player_profile import*
from Candies import*
from crosses import*

# Включить ведение журнала
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "Поставьте свой токен!"

def main() -> None:
# Старт бота
    updater = Updater(TOKEN)    # Создаём программу обновления и передаём ей токен нашего бота.
    dispatcher = updater.dispatcher # Просим диспетчера зарегистрировать обработчики
    # по разным командам - отвечайте в Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("hi", hi_command))
    dispatcher.add_handler(CommandHandler("time", time_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("sum", sum_command))
    player_profile_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('player_profile', player_profile_command)],
        states={
            PLAYER_NAME_STATE: [MessageHandler(Filters.text, input_player_name_handler)],
            PLAYER_AGE_STATE: [MessageHandler(Filters.text, input_player_age_handler)],
            PLAYER_GENDER_STATE: [MessageHandler(Filters.text, input_player_gender_handler)],},
        fallbacks=[],)
    dispatcher.add_handler(player_profile_conv_handler)

    game_candies_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('candies', game_candies)],
        states={
            GAME_CANDIES_STATE: [MessageHandler(Filters.text, game_candies)],
            GAME_TYPE_STATE: [MessageHandler(Filters.text, game_type)],
            CANDY_ISDIGIT_STATE: [MessageHandler(Filters.text, select_candy_isdigit)]},
        fallbacks=[])
    dispatcher.add_handler(game_candies_conv_handler)

    game_crosses_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('crosses', game_crosses)],
        states={
            GAME_CROSSES_STATE: [MessageHandler(Filters.text, game_crosses)],
            GAME_CROSSES_TYPE_STATE: [MessageHandler(Filters.text, game_crosses_type)],
            INPUT_CELL_STATE: [MessageHandler(Filters.text, input_cell)]},
        fallbacks=[])
    dispatcher.add_handler(game_crosses_conv_handler)
    # Запускаем бота
    print('server start')
    updater.start_polling()     # опрашиваем сервер телеграма

# Бот работает до тех пор, пока мы не нажмём Ctrl-C
# или процесс не получит SIGINT, SIGTERM или SIGABRT.
# Это следует использовать большую часть времени,
# так как start_polling() не блокирует и изящно остановит бота.
    updater.idle()

if __name__ == '__main__':
    main()
