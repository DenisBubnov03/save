from student_management import get_all_students
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from telegram.ext import ConversationHandler

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ['Добавить студента', 'Просмотреть студентов'],
        ['Редактировать данные студента', 'Проверить уведомления'],
        ['Поиск ученика'], ['Статистика']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=markup)



# Просмотр списка студентов
async def view_students(update: Update, context: ContextTypes.DEFAULT_TYPE):
    students = get_all_students()
    response = "Список студентов:\n"
    for i, student in enumerate(students, start=1):
        response += f"{i}. {student['ФИО']} - {student['Telegram']} ({student['Тип обучения']})\n"
    await update.message.reply_text(response)

async def exit_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возврат в главное меню и завершение ConversationHandler."""
    await start(update, context)  # Отображаем главное меню
    return ConversationHandler.END  # Завершаем ConversationHandler