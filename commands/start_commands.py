from student_management import get_all_students
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ['Добавить студента', 'Просмотреть студентов'],
        ['Редактировать данные студента', 'Проверить уведомления'],
        ['Поиск ученика', 'Помощь']
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
