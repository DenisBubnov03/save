from bot import WAIT_FOR_NEW_VALUE
from student_management import update_student_data
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from datetime import datetime
from commands.logger import logger


async def edit_student_employment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    student = context.user_data.get("student")
    logger.info(f"Вызвана edit_student_employment. Студент: {student}")
    if not student:
        await update.message.reply_text("Ошибка: студент не выбран. Попробуйте снова.")
        logger.error("Студент не выбран в edit_student_employment")
        return ConversationHandler.END

    # Проверка текущего статуса
    if student.get("Статус обучения") == "Устроился":
        await update.message.reply_text(
            "Студент уже устроился. Хотите изменить место работы?",
            reply_markup=ReplyKeyboardMarkup([["Да, изменить место работы"]], one_time_keyboard=True)
        )
        logger.info("Студент уже устроился. Ожидание подтверждения изменения места работы.")
        return "CONFIRMATION"

    # Если студент еще не устроился
    await update.message.reply_text(
        "Введите название компании, где устроился студент:"
    )
    logger.info("Ожидание ввода названия компании.")
    return "COMPANY_NAME"


async def handle_employment_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    if user_choice == "Да, изменить место работы":
        await update.message.reply_text(
            "Введите новое название компании:",)
        return "COMPANY_NAME"  # Переход в состояние ожидания ввода компании
    else:
        await update.message.reply_text(
            "Редактирование места работы отменено.",
            reply_markup=ReplyKeyboardMarkup([["Редактировать данные студента",]], one_time_keyboard=True)
        )
        return ConversationHandler.END



async def handle_company_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    student = context.user_data.get("student")
    logger.info(f"Вызвана handle_company_name. Студент: {student}")
    if not student:
        await update.message.reply_text("Ошибка: студент не выбран. Попробуйте снова.")
        logger.error("Студент не выбран в handle_company_name")
        return ConversationHandler.END

    company_name = update.message.text.strip()
    logger.info(f"Название компании: {company_name}")
    if not company_name:
        await update.message.reply_text("Название компании не может быть пустым. Попробуйте снова.")
        logger.warning("Пользователь ввел пустое название компании.")
        return "COMPANY_NAME"

    context.user_data["company_name"] = company_name
    await update.message.reply_text(
        "Введите зарплату студента (в числовом формате, например: 120000):",)
    logger.info("Ожидание ввода зарплаты.")
    return "SALARY"


async def handle_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    salary_text = update.message.text.strip()
    student = context.user_data.get("student")
    company_name = context.user_data.get("company_name")

    if not student or not company_name:
        await update.message.reply_text("Ошибка: данные студента или компании отсутствуют. Попробуйте снова.")
        return ConversationHandler.END

    if not salary_text.isdigit():
        await update.message.reply_text("Зарплата должна быть числом. Попробуйте снова.")
        return "SALARY"

    salary = int(salary_text)

    # Обновление данных в Google Sheets
    update_student_data(student["ФИО"], "Компания", company_name)
    update_student_data(student["ФИО"], "Зарплата", salary)
    update_student_data(student["ФИО"], "Статус обучения", "Устроился")
    update_student_data(student["ФИО"], "Дата устройства", datetime.now().strftime("%d.%m.%Y"))

    # Вывод уведомления об измененных данных
    await update.message.reply_text(
        f"Данные успешно обновлены! 🎉\n\n"
        f"Измененные данные:\n"
        f"👨‍🎓 Студент: {student['ФИО']}\n"
        f"🏢 Компания: {company_name}\n"
        f"💰 Зарплата: {salary}\n"
        f"📅 Дата устройства: {datetime.now().strftime('%d.%m.%Y')}\n"
        f"📘 Статус обучения: Устроился",
        reply_markup=ReplyKeyboardMarkup(
            [
                ["Добавить студента", "Просмотреть студентов"],
                ["Редактировать данные студента", "Проверить уведомления"]
            ],
            one_time_keyboard=True
        )
    )
    return ConversationHandler.END

