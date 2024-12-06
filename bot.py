from telegram.ext import Application, CommandHandler, MessageHandler, filters
from commands.student_statistic_commands import *
from commands.start_commands import start, view_students, exit_to_main_menu


from commands.student_editing_commands import *
from commands.student_employment_commands import *
from commands.student_info_commands import *
from commands.student_management_command import *
from commands.student_notifications import check_notifications

# Токен Telegram-бота
TELEGRAM_TOKEN = "7581276969:AAFHO1wVdwDbbV4c82IdY-lBOQX2HchgN0o"

# Состояния для ConversationHandler
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
            WAIT_FOR_NEW_VALUE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_value),
                MessageHandler(filters.Regex("^Получил работу$"), edit_student_employment),
                MessageHandler(filters.Regex("^Да, изменить место работы$"), handle_employment_confirmation),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_company_name),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_salary),
            ],
            "COMPANY_NAME": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_company_name)],
            "SALARY": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_salary)],
            "CONFIRMATION": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_employment_confirmation)],
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

    statistics_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Статистика$"), show_statistics_menu)],
        states={
            "STATISTICS_MENU": [
                MessageHandler(filters.Regex("^📈 Общая статистика$"), show_general_statistics),
                MessageHandler(filters.Regex("^📚 По типу обучения$"), show_course_type_menu),
            ],
            "COURSE_TYPE_MENU": [
                MessageHandler(filters.Regex("^👨‍💻 Ручное тестирование$"), show_manual_testing_statistics),
                MessageHandler(filters.Regex("^🤖 Автотестирование$"), show_automation_testing_statistics),
                MessageHandler(filters.Regex("^💻 Фуллстек$"), show_fullstack_statistics),
                MessageHandler(filters.Regex("^🔙 Назад$"), show_statistics_menu),
            ],
        },
        fallbacks=[
            MessageHandler(filters.Regex("^🔙 Вернуться в меню$"), exit_to_main_menu),  # Добавляем обработчик для выхода
        ],
    )


    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^Просмотреть студентов$"), view_students))
    application.add_handler(MessageHandler(filters.Regex("^Проверить уведомления$"), check_notifications))
    application.add_handler(add_student_handler)
    application.add_handler(edit_student_handler)
    application.add_handler(search_student_handler)
    application.add_handler(statistics_handler)


    # application.add_handler(MessageHandler(filters.Regex("Отмена"), cancel))  # Доп. проверка
    # application.add_handler(MessageHandler(filters.ALL, debug))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
