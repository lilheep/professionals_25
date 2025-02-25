from fastapi import FastAPI, HTTPException, Body
from models import User, Document, Comment, Employees, Positions, News
import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_user(name: str):
    user = User.get(User.name == name)
    return user

@app.post('/api/v1/SignIn')
async def sign_in(name: str = Body(...), password: str = Body(...)):
    user = get_user(name)
    if not user or user.password != password:
        raise HTTPException(status_code=403, detail='Неверное имя пользователя или пароль!')
    return {'message': 'Вы успешно авторизировались!'}

def get_document():
    return list(Document.select().dicts())

@app.get('/api/v1/Documents')
async def get_all_documents():
    return get_document()

def get_comment(id_doc: int):
    document = Document.get(Document.document_id == id_doc)
    comments = list(Comment.select().where(Comment.document_id == document.document_id))
    comments_json = [
        {
            'id': comment.comment_id,
            'document': id_doc,
            'text': comment.text,
            'date_created': comment.date_created,
            'date_updated': comment.date_updated,
            'author': {
                'author_id': comment.author_id,
                'author_position': comment.author_position
            }
        } for comment in comments
    ]
    return {
        'id': document.document_id,
        'title': document.title,
        'date_created': document.date_created,
        'date_updated': document.date_update,
        'category': document.category,
        'has_comments': document.has_comments,
        'comments': comments_json
    }
    
@app.get('/api/v1/Document/{documentId}/Comments')
async def get_comments_for_doc(documentId: int):
    return get_comment(id_doc=documentId)
    
@app.post('/api/v1/Document/{documentId}/Comment')
async def send_comment(doc_id: int, text_com: str, author: int, position: int):
    document = Document.get(Document.document_id == doc_id)
    if not document:
        raise HTTPException(status_code=404, detail='Документ не найден!')
    author_emp = Employees.get(Employees.employee_id == author)
    if not author_emp:
        raise HTTPException(status_code=404, detail='Авторизируйтесь, чтобы оставлять комментарии!')
    author_pos = Positions.get(Positions.position_id == position)
    if not position:
        raise HTTPException(status_code=2344, detail='Не найдено должности с указанным ID!')
    comment = Comment.get_or_create(document_id=doc_id, text=text_com, date_created=datetime.datetime.today(), date_updated=datetime.datetime.today(), author_id=author, author_position=position)
    return comment

@app.get('/api/get/News')
async def get_all_news():
    return list(News.select().dicts())

@app.get('/api/get/cardEmployee')
async def get_card_employee():
    employees = Employees.select(Employees, Positions.position_name).join(Positions, on=(Employees.position_id == Positions.position_id))
    employee_list = [{
        'last_name': employee.last_name,
        'first_name': employee.first_name,
        'middle_name': employee.middle_name,
        'birthday': employee.birthday,
        'position_name': employee.position_id.position_name,
        'number_phone': employee.business_phone_number,
        'corporate_mail': employee.corporate_mail
    } for employee in employees]
    return employee_list


