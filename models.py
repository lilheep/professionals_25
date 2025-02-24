from peewee import Model, CharField, AutoField, ForeignKeyField, IntegerField, DateField, Check, \
    TextField, DateTimeField, BooleanField
from database import db_connection
from datetime import datetime, timedelta
import re
import pandas as pd
import openpyxl

class BaseModel(Model):
    class Meta:
        database = db_connection
        
class Departments(BaseModel):
    department_id = AutoField()
    parent_department = CharField(max_length=255, null=False)
    department_name = CharField(max_length=255, null=False, unique=True)
    description = CharField(max_length=255, null=True)
    director_department = ForeignKeyField('self', on_delete='SET NULL', null=True, backref='departments')
    
class Positions(BaseModel):
    position_id = AutoField()
    position_name = CharField(max_length=255, null=False, unique=True)
    department_id = ForeignKeyField(Departments, on_delete='CASCADE', backref='position_department', null=True)

class Employees(BaseModel):
    employee_id = AutoField()
    last_name = CharField(max_length=255, null=False)
    first_name = CharField(max_length=255, null=False)
    middle_name = CharField(max_length=255, null=True)
    birthday_check = datetime.today().date() - timedelta(18*365.25)
    birthday = DateField(
        constraints=[Check(f"birthday <= '{birthday_check}'")]
        )
    business_phone_number = CharField(max_length=20, null=False)
    personal_phone_number = CharField(max_length=20, null=False)
    def validate(self):
        phone_regex = re.compile(r'^[0-9+\-()# ]{1,20}$')
        
        if not phone_regex.match(self.business_phone_number):
            raise ValueError('Error! Incorrect format phone number!')
        
        if not phone_regex.match(self.personal_phone_number):
            raise ValueError('Error! Incorrect format phone number!')
    cabinet = CharField(null=False, max_length=10)
    corporate_mail = CharField(max_length=255, null=False, 
                            constraints=[Check(r"corporate_mail REGEXP '^[A-Za-zА-Яа-яЁё0-9._%%+-]+@[A-Za-zА-Яа-яЁё-]+\\.[A-Za-zА-Яа-яЁё-]{2,}$'")])
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
    
class TrainingMaterials(BaseModel):
    material_id = AutoField()
    training_id = ForeignKeyField(TrainingsCalendar, backref='materials', on_delete='CASCADE')
    material_name = CharField(max_length=255, null=False)
    file_path = CharField(max_length=255, null=False)
    description = CharField(max_length=255, null=True)
    
class TrainingParticipants(BaseModel):
    participant_id = AutoField()
    employee_id = ForeignKeyField(Employees, backref='participant', on_delete='CASCADE')
    training_id = ForeignKeyField(TrainingsCalendar, backref='participant', on_delete='CASCADE')
    status = CharField(max_length=255, null=False, 
                       constraints=[Check("status IN ('Registered', 'Completed', 'Canceled')")])
    registation_date = DateField(null=False)
    
class MaterialCards(BaseModel):
    card_id = AutoField()
    training_material_id = ForeignKeyField(TrainingMaterials, backref='card', on_delete='CASCADE', null=True)
    material_name = CharField(max_length=255, null=False)
    approval_date = DateField(null=False)
    upload_date = DateField(null=False)
    status = CharField(max_length=255, null=False, 
                       constraints = [Check("status IN ('Approved', 'Checked', 'Canceled')")])
    material_type = CharField(max_length=255, null=False)
    area = CharField(max_length=255, null=False)
    author = ForeignKeyField(TrainingOrganizators, backref='uploaded_materials', on_delete='SET NULL', null=True)
    description = CharField(max_length=255, null=True)
    
class TrainingFeedback(BaseModel):
    feedback_id = AutoField()
    training_id = training_id = ForeignKeyField(TrainingsCalendar, backref='feedback', on_delete='CASCADE')
    employee_id = ForeignKeyField(Employees, backref='reviews', on_delete='CASCADE')
    rating = IntegerField(constraints=[Check("rating >= 1 AND rating <=5 ")], null=False)
    review_text = TextField(null=True)
    riview_date = DateField(null=False)
    
class AbsenceTypes(BaseModel):
    type_id = AutoField()
    type_name = CharField(max_length=255, null=False)
    description = CharField(max_length=255, null=False)

class AbsenceCalendar(BaseModel):
    absence_id = AutoField()
    employee_id = ForeignKeyField(Employees, backref='absence', on_delete='CASCADE')
    type_id = ForeignKeyField(AbsenceTypes, backref='type_absence', on_delete='SET NULL', null=True)
    start_date = DateTimeField(null=False)
    end_date = DateTimeField(null=False)
    reason = CharField(max_length=255, null=True)
    
class Substitutions(BaseModel):
    substitution_id = AutoField()
    absent_employee_id = ForeignKeyField(Employees, backref='absent_substitution', on_delete='CASCADE')
    substituting_employee_id = ForeignKeyField(Employees, backref='sub_substitution', on_delete='CASCADE')
    start_date = DateTimeField(null=False)
    end_date = DateTimeField(null=False)

class ActivityDirections(BaseModel):
    direction_id = AutoField()
    direction_name = CharField(max_length=255, null=False)
    description = CharField(max_length=255, null=True)
    
class CandidateStatus(BaseModel):
    status_id = AutoField()
    status_name = CharField(max_length=255, null=False, 
                            constraints=[Check("status_name IN ('Checked', 'Invited', 'Canceled')")])
    description = CharField(max_length=255, null=True)
    
class Candidates(BaseModel):
    candidate_id = AutoField()
    last_name = CharField(max_length=255, null=False)
    first_name = CharField(max_length=255, null=False)
    middle_name = CharField(max_length=255, null=True)
    email = CharField(max_length=255, null=False, 
                      constraints=[Check("email REGEXP '^[A-Za-z0-9._%%+-]+@[A-Za-z]\\.[A-Za-z]{2,}$'")])
    phone_number = CharField(max_length=20, null=False, 
                            constraints=[Check("phone_number REGEXP '^[0-9+()\\-#] + $'")])
    birthday_check = datetime.today().date() - timedelta(18*365.25)
    birthday = DateField(
        constraints=[Check(f"birthday >= '{birthday_check}'")])
    direction_id = ForeignKeyField(ActivityDirections, backref='candidates_direction', on_delete='SET NULL', null=True)
    status_id = ForeignKeyField(CandidateStatus, backref='candidates_status', on_delete='SET NULL', null=True)

class ResumeCandidates(BaseModel):
    resume_id = AutoField()
    candidate_id = ForeignKeyField(Candidates, backref='resume_candidate', on_delete='CASCADE')
    file_path = CharField(max_length=255, null=False)
    uploaded_resume = DateField(null=False)
    notes = CharField(max_length=255, null=True)

class EventsCalendar(BaseModel):
    event_id = AutoField()
    event_name = CharField(max_length=255, null=False)
    event_type = CharField(max_length=255, null=False)
    event_status = CharField(max_length=255, null=False, 
                            constraints=[Check("event_status IN ('Planned', 'Completed', 'Cancelled')")])
    start_time = DateTimeField(null=False)
    end_time = DateTimeField(null=False)
    description_event = TextField(null=False)
    responsible_employee = ForeignKeyField(Employees, backref='events', on_delete='SET NULL', null=True)
    departament_id = ForeignKeyField(Departments, backref='events', on_delete='SET NULL', null=True)
    
class WorkingCalendar(BaseModel):
    id = AutoField()
    exception_date = DateField(null=False)
    is_working_day = BooleanField(null=False )
    
    def validate(self):
        today = datetime.today().date()
        age_18 = today - timedelta(18*365.25)
        
        if self.birthday < age_18:
            raise ValueError('The employee must be of legal age!')
        
class User(BaseModel):
    user_id = AutoField()
    employee_id = ForeignKeyField(Employees, on_delete='CASCADE', backref='user_employee', null=True)
    name = CharField(max_length=255, null=False)
    password = CharField(max_length=255, null=False)
    
class Document(BaseModel):
    document_id = AutoField()
    title = CharField(max_length=255, null=False)
    date_created = DateTimeField(null=False)
    date_update = DateTimeField(null=False)
    category = CharField(max_length=255, null=False)
    has_comments = BooleanField(null=False)
    
class Comment(BaseModel):
    comment_id = AutoField()
    document_id = ForeignKeyField(Document, backref='comment_document', on_delete='CASCADE', null=True)
    text = TextField(null=False)
    date_created = DateTimeField(null=False)
    date_updated = DateTimeField(null=False)
    author_id = ForeignKeyField(User, backref='author_comment', on_delete='SET NULL', null=True)
    author_position = ForeignKeyField(Positions, backref='postition_author', on_delete='SET NULL', null=True)
       
tables = [
    Departments,
    Positions,
    Employees,
    EmployeesSchedules,
    EmployeeAdditionalInfo,
    TrainingCategories,
    TrainingOrganizators,
    TrainingsCalendar,
    TrainingMaterials,
    TrainingParticipants,
    MaterialCards,
    TrainingFeedback,
    AbsenceTypes,
    AbsenceCalendar,
    Substitutions,
    ActivityDirections,
    CandidateStatus,
    Candidates,
    ResumeCandidates,
    EventsCalendar,
    WorkingCalendar,
    User,
    Document,
    Comment
]

def create_tables():
    try:
        db_connection.create_tables(tables)
        print('Tables created successfully!')
    except Exception as e:
        print(f'Tables not created: {e}!')
        
def create_records():
    try:
        data = [
        (1, '2024-01-01', False),
        (2, '2024-01-02', False),
        (3, '2024-01-03', False),
        (4, '2024-01-04', False),
        (5, '2024-01-05', False),
        (6, '2024-01-08', False),
        (7, '2024-02-23', False),
        (8, '2024-03-08', False),
        (9, '2024-04-27', True),
        (10, '2024-04-29', False),
        (11, '2024-04-30', False),
        (12, '2024-05-01', False),
        (13, '2024-05-09', False),
        (14, '2024-05-10', False),
        (15, '2024-06-12', False),
        (16, '2024-11-02', True),
        (17, '2024-11-04', False),
        (18, '2024-12-28', True),
        (19, '2024-12-30', False),
        (20, '2024-12-31', False),
        ]
        
        with db_connection.atomic():
            for record in data:
                WorkingCalendar.get_or_create(id=record[0], exception_date=record[1], is_working_day=record[2])
            print('Records created!')
            
    except Exception as e:
        print(f'Records not created: {e}')
        
create_tables()
create_records()

# def add_employee(last_name, first_name, middle_name, birthday, business_phone_number, 
#                  personal_phone_number, cabinet, corporate_mail, department_id, 
#                  position_id, director_id=None, assistant_id=None, other_information=None):
#     employee = Employees.get_or_none(corporate_mail=corporate_mail)
    
#     if not employee:
#         employee = Employees.create(
#             last_name=last_name,
#             first_name=first_name,
#             middle_name=middle_name,
#             birthday=birthday,
#             business_phone_number=business_phone_number,
#             personal_phone_number=personal_phone_number,
#             cabinet=cabinet,
#             corporate_mail=corporate_mail,
#             department_id=department_id,
#             position_id=position_id,
#             director_id=director_id,
#             assistant_id=assistant_id,
#             other_information=other_information
#         )
#         employee.save()
#     return employee

# department = Departments.get_or_none(parent_department='Административный отдел', department_name='Административный департамент')
# if not department:
#     department = Departments.create(parent_department='Административный отдел', department_name='Административный департамент')
    
# position = Positions.get_or_none(position_name='Руководитель контрольно-ревизионного направления')
# if not position:
#     position = Positions.create(position_name='Руководитель контрольно-ревизионного направления')

# new_employee = add_employee(
#     last_name='Ivanov',
#     first_name='Ivan',
#     middle_name='Ivanovich',
#     birthday='1990-05-10',
#     business_phone_number='+7 (179) 370-26-88',
#     personal_phone_number='+7 (272) 192-26-66',
#     cabinet='A123',
#     corporate_mail='ivanov@example.com',
#     department_id=department,
#     position_id=position
# )

# print(f"Employee {new_employee.first_name} {new_employee.last_name} added successfully.")

if not db_connection.is_closed():
    db_connection.close()