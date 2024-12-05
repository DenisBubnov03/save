import gspread

# Подключение к Google Sheets
def connect_to_sheets():
    """Устанавливает подключение к таблице Google Sheets."""
    gc = gspread.service_account(filename="client_secret.json")
    spreadsheet = gc.open("Ученики")  # Название таблицы
    worksheet = spreadsheet.sheet1
    return worksheet

worksheet = connect_to_sheets()

# Добавление студента
def add_student(fio, telegram, start_date, course_type, total_payment, paid_amount, fully_paid):
    """Добавление нового студента в Google Sheets."""
    # Добавляем строку в таблицу
    worksheet.append_row([
        fio,              # ФИО
        telegram,         # Telegram
        start_date,       # Дата начала обучения
        course_type,      # Тип обучения
        total_payment,    # Стоимость обучения
        paid_amount,      # Сумма оплаты
        "",  # Дата последнего звонка (пустое значение при добавлении)
        "",  # Компания (пустое значение при добавлении)
        "",  # Дата трудоустройства (пустое значение при добавлении)
        "",  # Зарплата (пустое значение при добавлении)
        fully_paid,       # Полностью оплачено ("Да"/"Нет")
        "Учится"          # Статус обучения (по умолчанию "Учится")
    ])


# Удаление студента
def delete_student(identifier):
    """
    Удаляет студента по ФИО или Telegram из таблицы.

    Args:
        identifier (str): ФИО или Telegram студента.

    Returns:
        bool: True, если студент удалён, иначе False.
    """
    students = worksheet.get_all_records()
    for i, student in enumerate(students):
        if student["ФИО"] == identifier or student["Telegram"] == identifier:
            worksheet.delete_rows(i + 2)  # Удаляем строку (i + 2, так как 1-я строка - заголовок)
            return True
    return False

# Редактирование студента
def update_student_data(identifier, field, new_value):
    students = worksheet.get_all_records()
    for i, student in enumerate(students):
        if student["ФИО"] == identifier:
            headers = list(student.keys())
            if field in headers:
                col_index = headers.index(field) + 1
                worksheet.update_cell(i + 2, col_index, new_value)
                return True
    return False


# Получение списка всех студентов
def get_all_students():
    """
    Возвращает всех студентов в виде списка словарей.

    Returns:
        list: Список студентов (каждый студент - словарь с ключами, соответствующими столбцам).
    """
    return worksheet.get_all_records()
