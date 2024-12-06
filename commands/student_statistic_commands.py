from student_management import get_all_students
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


# Главное меню статистики
import logging

logger = logging.getLogger(__name__)

async def show_statistics_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню статистики."""
    logger.info("Показано меню статистики")
    await update.message.reply_text(
        "📊 Статистика:\nВыберите тип статистики:",
        reply_markup=ReplyKeyboardMarkup(
            [["📈 Общая статистика", "📚 По типу обучения"], ["🔙 Вернуться в меню"]],
            one_time_keyboard=True
        )
    )
    return "STATISTICS_MENU"



# Общая статистика
async def show_general_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображение общей статистики по всем студентам."""
    students = get_all_students()

    total_students = len(students)
    fully_paid = sum(1 for s in students if s.get("Полностью оплачено") == "Да")
    not_fully_paid = total_students - fully_paid

    await update.message.reply_text(
        f"📋 Общая статистика:\n\n"
        f"👥 Всего студентов: {total_students}\n"
        f"✅ Полностью оплатили: {fully_paid}\n"
        f"❌ Не оплатили полностью: {not_fully_paid}",
        reply_markup=ReplyKeyboardMarkup(
            [["🔙 Вернуться в меню"]],
            one_time_keyboard=True
        )
    )
    return "STATISTICS_MENU"


# Меню статистики по типу обучения
async def show_course_type_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вывод меню статистики по типу обучения."""
    await update.message.reply_text(
        "📚 Выберите тип обучения для статистики:",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["👨‍💻 Ручное тестирование", "🤖 Автотестирование", "💻 Фуллстек"],
                ["🔙 Назад"]
            ],
            one_time_keyboard=True
        )
    )
    return "COURSE_TYPE_MENU"


# Статистика по типу обучения
async def show_manual_testing_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Статистика по ручному тестированию."""
    students = get_all_students()
    manual_students = [s for s in students if s.get("Тип обучения") == "Ручное тестирование"]

    await update.message.reply_text(
        f"👨‍💻 Статистика по Ручному тестированию:\n\n"
        f"👥 Всего студентов: {len(manual_students)}",
        reply_markup=ReplyKeyboardMarkup(
            [["🔙 Назад"]],
            one_time_keyboard=True
        )
    )
    return "COURSE_TYPE_MENU"


async def show_automation_testing_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Статистика по автотестированию."""
    students = get_all_students()
    automation_students = [s for s in students if s.get("Тип обучения") == "Автотестирование"]

    await update.message.reply_text(
        f"🤖 Статистика по Автотестированию:\n\n"
        f"👥 Всего студентов: {len(automation_students)}",
        reply_markup=ReplyKeyboardMarkup(
            [["🔙 Назад"]],
            one_time_keyboard=True
        )
    )
    return "COURSE_TYPE_MENU"


async def show_fullstack_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Статистика по Фуллстек."""
    students = get_all_students()
    fullstack_students = [s for s in students if s.get("Тип обучения") == "Фуллстек"]

    await update.message.reply_text(
        f"💻 Статистика по Фуллстек:\n\n"
        f"👥 Всего студентов: {len(fullstack_students)}",
        reply_markup=ReplyKeyboardMarkup(
            [["🔙 Назад"]],
            one_time_keyboard=True
        )
    )
    return "COURSE_TYPE_MENU"

