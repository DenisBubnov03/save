from commands.states import FIO_OR_TELEGRAM
from student_management import get_all_students
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler




# Поиск и вывод информации об ученике
async def search_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите ФИО или Telegram ученика, информацию о котором хотите посмотреть:")
    return FIO_OR_TELEGRAM  # Состояние для поиска

async def display_student_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_query = update.message.text.lower()
    students = get_all_students()

    # Фильтрация студентов по совпадению с ФИО или Telegram
    matching_students = [
        student for student in students
        if search_query in student["ФИО"].lower() or search_query in student["Telegram"].lower()
    ]

    if not matching_students:
        await update.message.reply_text("Ученик не найден. Попробуйте ещё раз'.")
        return FIO_OR_TELEGRAM

    # Если найдено несколько студентов
    if len(matching_students) > 1:
        response = "Найдено несколько учеников. Уточните запрос:\n"
        for student in matching_students:
            response += f"{student['ФИО']} - {student['Telegram']}\n"
        await update.message.reply_text(response)
        return FIO_OR_TELEGRAM

    # Если найден один ученик
    student = matching_students[0]
    context.user_data["student"] = student  # Сохраняем ученика в контекст

    # Вывод всей информации об ученике
    info = "\n".join([f"{key}: {value}" for key, value in student.items()])
    await update.message.reply_text(
        f"Информация об ученике:\n\n{info}",
        reply_markup=ReplyKeyboardMarkup(
            [['Добавить студента', 'Просмотреть студентов'],
             ['Редактировать данные студента', 'Проверить уведомления'], ['Поиск ученика']],
            one_time_keyboard=True
        )
    )
    return ConversationHandler.END
