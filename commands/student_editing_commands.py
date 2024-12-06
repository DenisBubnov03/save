from commands.states import FIELD_TO_EDIT, WAIT_FOR_NEW_VALUE, FIO_OR_TELEGRAM
from commands.student_employment_commands import edit_student_employment
from student_management import get_all_students, update_student_data
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler


# Поиск студента
async def find_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_query = update.message.text.lower()
    students = get_all_students()

    matching_students = [
        student for student in students
        if search_query in student["ФИО"].lower() or search_query in student["Telegram"].lower()
    ]

    if not matching_students:
        await update.message.reply_text("Студент не найден. Попробуйте ещё раз:")
        return FIO_OR_TELEGRAM

    if len(matching_students) > 1:
        response = "Найдено несколько студентов. Уточните:\n"
        for i, student in enumerate(matching_students, start=1):
            response += f"{i}. {student['ФИО']} - {student['Telegram']}\n"
        await update.message.reply_text(response)
        return FIO_OR_TELEGRAM

    context.user_data["student"] = matching_students[0]
    await update.message.reply_text(
        f"Вы выбрали студента: {matching_students[0]['ФИО']} ({matching_students[0]['Telegram']}).\n"
        "Что вы хотите отредактировать?",
        reply_markup=ReplyKeyboardMarkup(
            [
                ['ФИО', 'Telegram', 'Дата последнего звонка', 'Сумма оплаты'],
                ['Получил работу']
            ],
            one_time_keyboard=True
        )
    )
    return FIELD_TO_EDIT


# Обработка команды редактирования
async def edit_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите ФИО или Telegram студента, данные которого вы хотите отредактировать:")
    return FIO_OR_TELEGRAM

async def edit_student_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    field_to_edit = update.message.text
    valid_fields = ["ФИО", "Telegram", "Дата последнего звонка", "Сумма оплаты", "Статус обучения"]

    if field_to_edit in valid_fields:
        context.user_data["field_to_edit"] = field_to_edit
        if field_to_edit == "Статус обучения":
            await update.message.reply_text(
                "Выберите новый статус:",
                reply_markup=ReplyKeyboardMarkup(
                    [["Учится", "Устроился", "Не учится"]],
                    one_time_keyboard=True
                )
            )
            return WAIT_FOR_NEW_VALUE
        else:
            await update.message.reply_text(
                f"Введите новое значение для '{field_to_edit}':"
            )
            return WAIT_FOR_NEW_VALUE
    elif field_to_edit == "Получил работу":
        return await edit_student_employment(update, context)  # Логика перенаправлена
    else:
        await update.message.reply_text(
            "Некорректное поле. Выберите одно из предложенных.",
            reply_markup=ReplyKeyboardMarkup(
                [["ФИО", "Telegram", "Дата последнего звонка", "Сумма оплаты", "Статус обучения"]],
                one_time_keyboard=True
            )
        )
        return FIELD_TO_EDIT



async def handle_new_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    student = context.user_data.get("student")
    field_to_edit = context.user_data.get("field_to_edit")
    new_value = update.message.text

    if not student or not field_to_edit:
        await update.message.reply_text("Ошибка: данные для редактирования отсутствуют. Начните сначала.")
        return ConversationHandler.END

    if field_to_edit == "Сумма оплаты":
        try:
            additional_payment = int(new_value)
            current_payment = int(student.get("Сумма оплаты", 0))
            total_payment = int(student.get("Стоимость обучения", 0))

            if current_payment + additional_payment > total_payment:
                await update.message.reply_text(
                    f"Ошибка: итоговая сумма оплаты ({current_payment + additional_payment}) "
                    f"превышает стоимость обучения ({total_payment}). Введите корректное значение."
                )
                return FIELD_TO_EDIT

            updated_payment = current_payment + additional_payment
            fully_paid = "Да" if updated_payment == total_payment else "Нет"

            update_student_data(student["ФИО"], "Сумма оплаты", updated_payment)
            update_student_data(student["ФИО"], "Полностью оплачено", fully_paid)

            await update.message.reply_text(
                f"Сумма оплаты успешно обновлена! Теперь оплачено: {updated_payment} из {total_payment}.",
                reply_markup=ReplyKeyboardMarkup(
                    [['Добавить студента', 'Просмотреть студентов'],
                     ['Редактировать данные студента', 'Проверить уведомления'], ['Статистика']],
                    one_time_keyboard=True
                )
            )
            return ConversationHandler.END
        except ValueError:
            await update.message.reply_text("Введите корректное число. Попробуйте снова.")
            return FIELD_TO_EDIT



