from peewee import Model, CharField, AutoField, ForeignKeyField, IntegerField, DateField, Check, \
    TextField, DateTimeField
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
    
    def validate(self):
        today = datetime.today().date()
        age_18 = today - timedelta(18*365.25)
        
        if self.birthday < age_18:
            raise ValueError('The employee must be of legal age!')
       
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
    EventsCalendar
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