from peewee import Model, CharField, AutoField, ForeignKeyField, IntegerField, DateField, Check
from database import db_connection
from datetime import datetime, timedelta


class BaseModel(Model):
    class Meta:
        database = db_connection
        
class Departments(BaseModel):
    department_id = AutoField()
    department_name = CharField(max_length=255, null=False, unique=True)
    description = CharField(max_length=255, null=True)
    director_department = ForeignKeyField('self', on_delete='SET NULL', null=True, backref='departments')
    
class Positions(BaseModel):
    position_id = AutoField()
    position_name = CharField(max_length=255, null=False, unique=True)

class Employees(BaseModel):
    employee_id = AutoField()
    last_name = CharField(max_length=255, null=False)
    first_name = CharField(max_length=255, null=False)
    middle_name = CharField(max_length=255, null=True)
    birthday_check = datetime.today().date() - timedelta(18*365.25)
    birthday = DateField(
        constraints=[Check(f"birthday >= '{birthday_check}'")]
        )
    business_phone_number = CharField(max_length=20, null=False, 
                                    constraints=[Check("business_phone_number ~ '^[0-9+()\\-#] + $'")])
    personal_phone_number = CharField(max_length=20, null=False, 
                                    constraints=[Check("personal_phone_number ~ '^[0-9+()\\-#] + $'")])
    cabinet = CharField(null=False, max_length=10)
    corporate_mail = CharField(max_length=255, null=False, unique = True, 
                            constraints=[Check("corporate_mail ~ '^[A-Za-z0-9._%+-]+@[A-Za-z]+\\.[A-Za-z]{2,}$'")])
    department_id = ForeignKeyField(Departments, on_delete='SET NULL', backref='employees', null=True)
    position_id = ForeignKeyField(Positions, on_delete='SET NULL', backref='employees', null=True)
    director_id = ForeignKeyField('self', backref='subordinates', on_delete='SET NULL', null=True)
    assistant_id = ForeignKeyField('self', backref='assists', on_delete='SET NULL', null=True)
    other_information = CharField(max_length=255, null=True)
    
    def validate(self):
        today = datetime.today().date()
        age_18 = today - timedelta(18*365.25)
        
        if self.birthday < age_18:
            raise ValueError('The employee must be of legal age!')
           
class EmployeesSchedules(BaseModel):
    id_schedule = AutoField()
    employee_id = ForeignKeyField(Employees, backref='schedules', on_delete='CASCADE')
    type_event = CharField(max_length=255, null=False)
    start_date = DateField()
    end_date = DateField()

# Information that an employee can change    
class EmployeeAdditionalInfo(BaseModel):
    additional_id = AutoField()
    employee_id = ForeignKeyField(Employees, backref='', on_delete='CASCADE')
    personal_phone_number = CharField(max_length=20, null=True, 
                                    constraints=[Check("personal_phone_number ~ '^[0-9+()\\-#] + $'")])
    birthday = DateField(null=True)
    
tables = [
    Departments,
    Positions,
    Employees,
    EmployeesSchedules,
    EmployeeAdditionalInfo
]

def create_tables():
    db_connection.create_tables(tables)
    print('Tables created successfully!')
    
    
create_tables()

if not db_connection.is_closed():
    db_connection.close()