from datetime import datetime
from student_management import get_all_students
from telegram import Update
from telegram.ext import ContextTypes



# Проверка уведомлений
async def check_notifications(update: Update, context: ContextTypes.DEFAULT_TYPE):
    students = get_all_students()
    payment_notifications = []
    call_notifications = []

    for student in students:
        if student["Полностью оплачено"] == "Нет":
            due_amount = int(student["Стоимость обучения"]) - int(student["Сумма оплаты"])
            payment_notifications.append(f"Студент {student['ФИО']} должен {due_amount} рублей.")

    for student in students:
        # Проверяем, если статус "Учится"
        if student["Статус обучения"] == "Учится":
            last_call_date = student.get("Дата последнего звонка")

            if not last_call_date:
                # Если дата звонка отсутствует
                call_notifications.append(f"Студент {student['ФИО']} не звонил.")
            else:
                try:
                    # Преобразуем дату последнего звонка
                    last_call = datetime.strptime(last_call_date, "%d.%m.%Y")
                    days_since_last_call = (datetime.now() - last_call).days

                    # Проверяем, если прошло больше 20 дней
                    if days_since_last_call > 20:
                        call_notifications.append(
                            f"Студент {student['ФИО']} не звонил {days_since_last_call} дней. Пора позвонить!"
                        )
                except ValueError:
                    # Если формат даты некорректен
                    call_notifications.append(
                        f"Студент {student['ФИО']} имеет некорректную дату звонка: {last_call_date}"
                    )

    messages = []

    if payment_notifications:
        messages.append("❗ Уведомления по оплатам:")
        messages.extend(payment_notifications)

    if call_notifications:
        messages.append("❗ Уведомления по звонкам:")
        messages.extend(call_notifications)

    if not messages:
        await update.message.reply_text("✅ Все в порядке, уведомлений нет!")
    else:
        await update.message.reply_text("\n".join(messages))
