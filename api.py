from fastapi import FastAPI, HTTPException, Body
from models import User, Document, Comment, Employees, Positions
import datetime

app = FastAPI()

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



    


