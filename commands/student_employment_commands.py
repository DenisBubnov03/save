from student_management import  update_student_data
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler


async def edit_student_employment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите название компании, где устроился студент:"
    )
    return "COMPANY_NAME"


async def handle_company_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["company"] = update.message.text
    await update.message.reply_text(
        "Введите зарплату студента (например, 120k):"
    )
    return "SALARY"


async def handle_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    salary = update.message.text
    if not salary.endswith("k") or not salary[:-1].isdigit():
        await update.message.reply_text("Зарплата должна быть в формате, например: 120k. Попробуйте снова.")
        return "SALARY"

    context.user_data["salary"] = salary

    # Обновляем данные студента в Google Sheets
    student = context.user_data["student"]
    update_student_data(student["ФИО"], "Статус обучения", "Устроился")
    update_student_data(student["ФИО"], "Компания", context.user_data["company"])
    update_student_data(student["ФИО"], "Зарплата", salary)

    await update.message.reply_text(
        f"Данные успешно обновлены! 🎉\n"
        f"Компания: {context.user_data['company']}\n"
        f"Зарплата: {salary}\n"
        f"Статус обучения: Устроился",
        reply_markup=ReplyKeyboardMarkup(
            [['Редактировать данные студента', 'Вернуться в меню']],
            one_time_keyboard=True
        )
    )
    return ConversationHandler.END