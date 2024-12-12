from flask import Flask, request
import asyncio
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from commands.start_commands import start, exit_to_main_menu
from commands.states import NOTIFICATION_MENU
from commands.student_commands import *
from commands.student_employment_commands import *
from commands.student_info_commands import *
from commands.student_management_command import *
from commands.student_notifications import check_call_notifications, check_payment_notifications, \
    check_all_notifications, show_notifications_menu
from commands.student_selection import *
from commands.student_statistic_commands import show_statistics_menu, show_general_statistics, show_course_type_menu, \
    show_manual_testing_statistics, show_automation_testing_statistics, show_fullstack_statistics
# Переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.getenv("PORT", 5000))

# Инициализация Flask
app = Flask(__name__)

# Telegram Application
application = Application.builder().token(TELEGRAM_TOKEN).build()

# Маршрут для проверки доступности
@app.route("/")
def home():
    return "Telegram Bot is Running!"

# Маршрут для обработки вебхуков
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    """
    Обрабатывает запросы Telegram через вебхуки.
    """
    json_data = request.get_json()
    asyncio.run(application.update_queue.put(json_data))
    return "OK", 200

# Установка вебхука
async def set_webhook():
    """
    Устанавливает вебхук для Telegram.
    """
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_URL')}/{TELEGRAM_TOKEN}"
    print(f"Webhook установлен: {webhook_url}")
    await application.bot.set_webhook(webhook_url)

# Основные обработчики Telegram
def setup_handlers():
    """
    Настройка всех обработчиков для Telegram бота.
    """
    application.add_handler(CommandHandler("start", start))

    # Пример добавления обработчиков
    application.add_handler(MessageHandler(filters.Regex("^Просмотреть студентов$"), view_students))

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
            COMMISSION: [MessageHandler(filters.TEXT, add_student_commission)],
        },
        fallbacks=[],
    )

    # Обработчик редактирования студента
    edit_student_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Редактировать данные студента$"), edit_student)],
        states={
            FIO_OR_TELEGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, find_student)],
            SELECT_STUDENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_multiple_students)],
            FIELD_TO_EDIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_student_field)],
            WAIT_FOR_NEW_VALUE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_new_value),
            ],
            "COMPANY_NAME": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_company_name)],
            "SALARY": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_salary)],
            "COMMISSION": [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_commission)],
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
    notifications_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^Проверить уведомления$"), show_notifications_menu)],
        states={
            NOTIFICATION_MENU: [
                MessageHandler(filters.Regex("^По звонкам$"), check_call_notifications),
                MessageHandler(filters.Regex("^По оплате$"), check_payment_notifications),
                MessageHandler(filters.Regex("^Все$"), check_all_notifications),
            ],
            "NOTIFICATION_PROCESS": [
                MessageHandler(filters.Regex("^🔙 Назад$"), show_notifications_menu),
            ],
        },
        fallbacks=[
            MessageHandler(filters.Regex("^🔙 Главное меню$"), exit_to_main_menu),
        ],
    )

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^Просмотреть студентов$"), view_students))
    application.add_handler(add_student_handler)
    application.add_handler(edit_student_handler)
    application.add_handler(search_student_handler)
    application.add_handler(statistics_handler)
    application.add_handler(notifications_handler)
    application.add_handler(add_student_handler)

    # Добавьте обработчики для других функций, таких как редактирование студента,
    # просмотр статистики, проверка уведомлений и т.д.

# Главная точка входа
if __name__ == "__main__":
    # Установка обработчиков
    setup_handlers()

    # Установка вебхука
    print(f"Starting Flask on port {PORT}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_webhook())

    # Запуск Flask сервера
    app.run(host="0.0.0.0", port=PORT)
