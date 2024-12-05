from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

from commands.start_commands import start, view_students
from commands.states import TELEGRAM, FIO, START_DATE, COURSE_TYPE, TOTAL_PAYMENT, PAID_AMOUNT, FIELD_TO_EDIT, WAIT_FOR_NEW_VALUE
import os

from commands.student_editing_commands import *
from commands.student_employment_commands import *
from commands.student_info_commands import search_student, display_student_info
from commands.student_management_command import *
from commands.student_notifications import check_notifications

# Токен Telegram-бота
TELEGRAM_TOKEN = "7581276969:AAFHO1wVdwDbbV4c82IdY-lBOQX2HchgN0o"

# Состояния для ConversationHandler
TELEGRAM, FIO, FIO_OR_TELEGRAM, FIELD_TO_EDIT, START_DATE, COURSE_TYPE, TOTAL_PAYMENT, PAID_AMOUNT, WAIT_FOR_NEW_VALUE = range(9)


def main():
    # Создание приложения Telegram
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обработчик добавления студента
    add_student_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Добавить студента$"), add_student_start)],
        states={
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_student_fio)],
            TELEGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_student_telegram)],
            START_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_student_date)],
            COURSE_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_student_course_type)],
            TOTAL_PAYMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_student_total_payment)],
            PAID_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_student_paid_amount)],
        },
        fallbacks=[],
    )

    # Обработчик редактирования студента
    edit_student_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Редактировать данные студента$"), edit_student)],
        states={
            FIO_OR_TELEGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, find_student)],
            FIELD_TO_EDIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_student_field)],
            WAIT_FOR_NEW_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_value)],
            "COMPANY_NAME": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_company_name)],
            "SALARY": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_salary)],
        },
        fallbacks=[],
    )

    search_student_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Поиск ученика$"), search_student)],
        states={
            FIO_OR_TELEGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, display_student_info)],
        },
        fallbacks=[],
    )

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^Просмотреть студентов$"), view_students))
    application.add_handler(MessageHandler(filters.Regex("^Проверить уведомления$"), check_notifications))
    application.add_handler(add_student_handler)
    application.add_handler(edit_student_handler)
    application.add_handler(search_student_handler)

    # application.add_handler(MessageHandler(filters.Regex("Отмена"), cancel))  # Доп. проверка
    # application.add_handler(MessageHandler(filters.ALL, debug))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
