import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

PROJECT_DESCRIPTION = """
🚶‍♂️ *"Прогулки по Москве"* - это студенческий проект в рамках Проектной Практики, посвященный созданию 2D-игры о Басманном районе Москвы.

📌 *Основные особенности проекта:*
- Исследование исторического наследия Басманного района
- Реализация нескольких временных эпох в игровом процессе
- Образовательный и развлекательный контент
- Разработка силами студенческой команды

🕹 Игра позволит виртуально прогуляться по улицам Басманного района, увидеть его архитектуру и узнать интересные исторические факты.
"""

EPOCHS_INFO = """
🕰 *Доступные временные эпохи в игре:*

1. *XVIII-XIX века* - Эпоха становления района, классицизм и расцвет купеческой Москвы
2. *Современность* - Басманный район сегодня
3. *Чертежи прошлого* - Какой мог быть район, по чертежам прошлого 


Каждая эпоха представлена с характерной архитектурой, известными личностями и событиями того времени.
"""

TEAM_INFO = """
👥 *Команда проекта:*

- Программисты: разработка игрового движка и логики
- Дизайнеры: создание 2D-артов и анимаций
- Сценаристы: исследование и подготовка контента
- Аналитики: сбор данных, наблюдение за ходом работы

Проект реализуется студентами в рамках учебной практики.
"""

LINKS_INFO = """
🔗 *Полезные ссылки:*

- [GitHub репозиторий](https://github.com/kofresh/PD-mskprog)
"""

def get_main_menu_keyboard():
    """Создает клавиатуру главного меню"""
    keyboard = [
        [
            InlineKeyboardButton("О проекте", callback_data="about"),
            InlineKeyboardButton("Эпохи", callback_data="epochs"),
        ],
        [
            InlineKeyboardButton("Команда", callback_data="team"),
            InlineKeyboardButton("Репозиторий", callback_data="links"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_menu_keyboard():
    """Создает клавиатуру с кнопкой возврата в меню"""
    keyboard = [
        [InlineKeyboardButton("← Назад в меню", callback_data="menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await show_main_menu(update, context)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str = None):
    """Показывает главное меню"""
    if not text:
        text = "Привет! Я бот проекта 'Прогулки по Москве' 🏛\n\nВыбери, о чем хочешь узнать:"
    
    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=get_main_menu_keyboard(),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "menu":
        await show_main_menu(update, context)
        return
    
    if query.data == "about":
        text = PROJECT_DESCRIPTION
    elif query.data == "epochs":
        text = EPOCHS_INFO
    elif query.data == "team":
        text = TEAM_INFO
    elif query.data == "links":
        text = LINKS_INFO
    else:
        text = "Неизвестная команда"
        await show_main_menu(update, context, text)
        return
    
    await query.edit_message_text(
        text=text,
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    await update.message.reply_text(
        "Используй кнопки для навигации или команды:\n"
        "/start - начать общение\n"
        "/about - о проекте\n"
        "/epochs - о временных эпохах\n"
        "/team - о команде\n"
        "/links - полезные ссылки\n\n"
        "В любой момент можно вернуться в главное меню, нажав кнопку 'Назад'",
        reply_markup=get_back_to_menu_keyboard()
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /about"""
    await update.message.reply_text(
        PROJECT_DESCRIPTION,
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def epochs_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /epochs"""
    await update.message.reply_text(
        EPOCHS_INFO,
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def team_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /team"""
    await update.message.reply_text(
        TEAM_INFO,
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def links_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /links"""
    await update.message.reply_text(
        LINKS_INFO,
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    text = update.message.text.lower()
    if any(word in text for word in ["привет", "здравствуй", "hello", "hi"]):
        await update.message.reply_text(
            "Привет! Напиши /start для начала работы.",
            reply_markup=get_main_menu_keyboard()
        )
    elif any(word in text for word in ["меню", "начать", "start", "главная"]):
        await show_main_menu(update, context)
    else:
        await update.message.reply_text(
            "Извини, я не понимаю. Попробуй команду /help",
            reply_markup=get_main_menu_keyboard()
        )

def main() -> None:
    """Запуск бота"""
    application = Application.builder().token("8157201939:AAHliOOO9IbC2APi8GgFlrcd45DM4LSLpH8").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("epochs", epochs_command))
    application.add_handler(CommandHandler("team", team_command))
    application.add_handler(CommandHandler("links", links_command))
    
    application.add_handler(CallbackQueryHandler(button))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == "__main__":
    main()
