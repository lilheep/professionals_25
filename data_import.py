from database import db_connection
import pandas as pd
from models import Employees, Positions

def read_excel(file_path):
    """Читаем Excel-файл, учитывая заголовки на 4-х уровнях"""
    df = pd.read_excel(file_path, sheet_name='TDSheet', header=[2, 3, 4, 5])
    df.columns = ['_'.join([str(c) for c in col if str(c) != 'Unnamed']).strip() for col in df.columns]
    return df

def filter_employees(df):
    """Удаляем пустые строки и строки с заголовками"""
    df = df[df.iloc[:, 1].notna()]
    df = df[df.iloc[:, 1] != 'Сотрудник']
    df = df.reset_index(drop=True)
    print("\nВсе колонки в DataFrame:")
    print(df.columns.tolist())
    return df

def process_data(df):
    """Обрабатываем данные"""
    df = filter_employees(df)

    employee_col = next((col for col in df.columns if 'Сотрудник' in col), None)
    if not employee_col:
        raise KeyError("Столбец с ФИО сотрудника не найден! Проверьте структуру файла.")

    print(f"Найден столбец с ФИО: {employee_col}")

    df[['last_name', 'first_name', 'middle_name']] = df[employee_col].str.split(' ', expand=True)

    dob_col = next((col for col in df.columns if 'Дата рождения' in col), None)
    if dob_col:
        df[dob_col] = pd.to_datetime(df[dob_col], errors='coerce').dt.date

    phone_col = next((col for col in df.columns if 'Телефон рабочий' in col), None)
    if phone_col:
        df[phone_col] = df[phone_col].astype(str).str.strip()

    email_col = next((col for col in df.columns if 'Корпоративный email' in col), None)
    if email_col:
        df[email_col] = df[email_col].astype(str).str.strip()

    return df

def load_data_to_db(df):
    with db_connection.atomic():
        for index, row in df.iterrows():
            print(f"\nОбработка сотрудника {index + 1}: {row['last_name']} {row['first_name']}")

            print(f"Полная строка данных: {dict(row)}")

            position_name = row.get('Unnamed: 0_level_0_Организация_Подразделение организации_Должность', 'Не указана').strip()
            position, created_pos = Positions.get_or_create(position_name=position_name)

            if created_pos:
                print(f"Создана должность: {position.position_name} (ID: {position.position_id})")
            else:
                print(f"Должность уже существует: {position.position_name} (ID: {position.position_id})")

            Employees.create(
                last_name=row['last_name'],
                first_name=row['first_name'],
                middle_name=row.get('middle_name', ''),
                birthday=row.get('Unnamed: 2_level_0_Дата рождения_Unnamed: 2_level_2_Unnamed: 2_level_3'),
                business_phone_number=row.get('Unnamed: 3_level_0_Телефон рабочий_Unnamed: 3_level_2_Unnamed: 3_level_3', ''),
                personal_phone_number=row.get('Unnamed: 3_level_0_Телефон рабочий_Unnamed: 3_level_2_Unnamed: 3_level_3', ''),
                cabinet=row.get('Unnamed: 4_level_0_Кабинет_Unnamed: 4_level_2_Unnamed: 4_level_3', ''),
                corporate_mail=row.get('Unnamed: 5_level_0_Корпоративный email_Unnamed: 5_level_2_Unnamed: 5_level_3', ''),
                position_id=position
            )
            print("Сотрудник добавлен в базу!")

    print("\nВсе сотрудники загружены в БД!")

def main():
    file_path = 'data/org_structure.xlsx'

    df = read_excel(file_path)
    df = process_data(df)
    load_data_to_db(df)
    print(f"\nФайл загружен! Колонки: {df.columns.tolist()}")

    print("\nДанные успешно загружены в БД!")

if __name__ == "__main__":
    main()
