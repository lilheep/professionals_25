import pandas as pd
from models import Departments, Employees, Positions
from database import db_connection

def import_excel_to_db(file_path):
    try:
        data = pd.read_excel(file_path, header=4)
        data.columns = data.columns.str.strip()
        print(f'Столбцы в файле: {data.columns}')
    except Exception as e:
        print(f'Error read file: {e}')
        return

    for index, row in data.iterrows():
        department, created = Departments.get_or_create(
            department_name=row['Подразделение организации'],
            defaults={'description': None, 'director_department': None}
        )

        position, created = Positions.get_or_create(
            position_name=row['Должность']
        )
        
        try:
            Employees.create(
                last_name=row['Сотрудник'].split()[0],
                first_name=row['Сотрудник'].split()[1],
                middle_name=row['Сотрудник'].split()[2] if len(row['Сотрудник'].split()) > 2 else None,
                birthday=pd.to_datetime(row['Дата рождения']).date(),
                business_phone_number=row['Телефон рабочий'],
                cabinet=row['Кабинет'],
                corporate_mail=row['Корпоративный email'],
                department_id=department.departament_id,
                position_id = position.position_id
            )
        except Exception as e:
            print(f'Error load data ({row["Сотрудник"]}): {e}')
            
file_path = 'data/org_structure.xlsx'
import_excel_to_db(file_path)
            