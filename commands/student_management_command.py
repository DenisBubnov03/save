from datetime import datetime

from commands.states import *
from student_management import add_student
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

# Добавление студента: шаг 1 - ввод ФИО
async def add_student_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите ФИО студента:",
    )
    return FIO


# Добавление студента: шаг 2 - ввод Telegram
async def add_student_fio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["fio"] = update.message.text
    await update.message.reply_text(
        "Введите Telegram студента:",)
    return TELEGRAM


# Добавление студента: шаг 3 - ввод даты начала обучения
async def add_student_telegram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_account = update.message.text
    if telegram_account.startswith("@") and len(telegram_account) > 1:
        context.user_data["telegram"] = telegram_account
        await update.message.reply_text(
            "Введите дату начала обучения (в формате ДД.ММ.ГГГГ):",)
        return START_DATE
    else:
        await update.message.reply_text(
            "Некорректный Telegram. Убедитесь, что он начинается с @. Попробуйте ещё раз.")
        return TELEGRAM


# Добавление студента: шаг 4 - выбор типа обучения
async def add_student_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        date_text = update.message.text
        datetime.strptime(date_text, "%d.%m.%Y")
        context.user_data["start_date"] = date_text
        await update.message.reply_text(
            "Выберите тип обучения:",
            reply_markup=ReplyKeyboardMarkup(
                [['Ручное тестирование', 'Автотестирование', 'Фуллстек',]],
                one_time_keyboard=True
            )
        )
        return COURSE_TYPE
    except ValueError:
        await update.message.reply_text(
            "Дата должна быть в формате ДД.ММ.ГГГГ. Попробуйте ещё раз.",)
        return START_DATE


# Добавление студента: шаг 5 - выбор стоимости обучения
async def add_student_course_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    valid_course_types = ["Ручное тестирование", "Автотестирование", "Фуллстек"]
    course_type = update.message.text

    if course_type in valid_course_types:
        context.user_data["course_type"] = course_type
        await update.message.reply_text(
            "Введите общую стоимость обучения:",)
        return TOTAL_PAYMENT
    else:
        await update.message.reply_text(
            f"Некорректный тип обучения. Выберите один из вариантов: {', '.join(valid_course_types)}.")
        return COURSE_TYPE


# Добавление студента: шаг 6 - ввод общей стоимости
async def add_student_total_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        total_payment = int(update.message.text)
        if total_payment > 0:
            context.user_data["total_payment"] = total_payment
            await update.message.reply_text(
                "Введите сумму уже внесённой оплаты:",)
            return PAID_AMOUNT
        else:
            await update.message.reply_text(
                "Сумма должна быть больше 0. Попробуйте ещё раз.",)
            return TOTAL_PAYMENT
    except ValueError:
        await update.message.reply_text(
            "Введите корректное число. Попробуйте ещё раз.")
        return TOTAL_PAYMENT


# Завершение добавления студента
async def add_student_paid_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        paid_amount = int(update.message.text)
        total_payment = context.user_data["total_payment"]

        if 0 <= paid_amount <= total_payment:
            fully_paid = "Да" if paid_amount == total_payment else "Нет"
            context.user_data["paid_amount"] = paid_amount

            # Сохранение данных в Google Sheets
            add_student(
                context.user_data["fio"],
                context.user_data["telegram"],
                context.user_data["start_date"],
                context.user_data["course_type"],
                total_payment,
                paid_amount,
                fully_paid
            )

            await update.message.reply_text(
                "Студент успешно добавлен!",
                reply_markup=ReplyKeyboardMarkup(
                    [['Добавить студента', 'Просмотреть студентов'],
                     ['Редактировать данные студента', 'Проверить уведомления']],
                    one_time_keyboard=True
                )
            )
            return ConversationHandler.END
        else:
            await update.message.reply_text(
                f"Сумма оплаты должна быть в пределах от 0 до {total_payment}. Попробуйте ещё раз."
            )
            return PAID_AMOUNT
    except ValueError:
        await update.message.reply_text(
            "Введите корректное число. Попробуйте ещё раз."
        )
        return PAID_AMOUNT
