from peewee import Model, CharField, AutoField, ForeignKeyField, IntegerField
from database import db_connection

class BaseModel(Model):
    class Meta:
        database = db_connection
        
class Employees(BaseModel):
    employee = AutoField()
    last_name = CharField(max_length=255, null=False)
    first_name = CharField(max_length=255, null=False)
    middle_name = CharField(max_length=255, null=True)
    business_phone_number = CharField(max_length=11, null=False)
    personal_phone_number = CharField(max_length=11, null=False)
    cabinet = IntegerField(null=False)
    corporate_mail = CharField(max_length=255, null=False)
    departament_id = ForeignKeyField()
    position_id = ForeignKeyField()
    director_id = IntegerField()
    assistant_id = IntegerField()
    other_information = CharField(max_length=255, null=True)