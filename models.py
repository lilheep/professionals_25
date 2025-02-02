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
                                    constraints=[Check("business_phone_number REGEXP '^[0-9+()\\-#] + $'")])
    personal_phone_number = CharField(max_length=20, null=False, 
                                    constraints=[Check("personal_phone_number REGEXP '^[0-9+()\\-#] + $'")])
    cabinet = CharField(null=False, max_length=10)
    corporate_mail = CharField(max_length=255, null=False, unique = True, 
                            constraints=[Check("corporate_mail REGEXP '^[A-Za-z0-9._%%+-]+@[A-Za-z]+\\.[A-Za-z]{2,}$'")])
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
                                    constraints=[Check("personal_phone_number REGEXP '^[0-9+()\\-#] + $'")])
    birthday_check = datetime.today().date() - timedelta(18*365.25)
    birthday = DateField(
        constraints=[Check(f"birthday >= '{birthday_check}'")]
        )
    
    def validate(self):
        today = datetime.today().date()
        age_18 = today - timedelta(18*365.25)
        
        if self.birthday < age_18:
            raise ValueError('The employee must be of legal age!')
        
class TrainingCategories(BaseModel):
    category_id = AutoField()
    category_name = CharField(max_length=255, null=False)
    description = CharField(max_length=255, null=False)
    
class TrainingOrganizators(BaseModel):
    organizator_id = AutoField()
    internal_organizator = ForeignKeyField(Employees, backref='organtizator', on_delete='SET NULL', null=True)
    external_organizator = CharField(max_length=255, null=True)

class TrainingsCalendar(BaseModel):
    training_id = AutoField()
    training_name = CharField(max_length=255, null=False)
    category_id = ForeignKeyField(TrainingCategories, on_delete='SET NULL', null=True, backref='training')
    start_date = DateField(null=False)
    end_date = DateField(null=False)
    location = CharField(max_length=255, null=False)
    organizator = ForeignKeyField(TrainingOrganizators, backref='organization', on_delete='CASCADE')
    
    
tables = [
    Departments,
    Positions,
    Employees,
    EmployeesSchedules,
    EmployeeAdditionalInfo
]

def create_tables():
    try:
        db_connection.create_tables(tables)
        print('Tables created successfully!')
    except Exception as e:
        print(f'Tables not created: {e}!')
    
create_tables()

if not db_connection.is_closed():
    db_connection.close()