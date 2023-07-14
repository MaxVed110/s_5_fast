# Task_6
# Создайте модуль приложения и настройте сервер и маршрутизацию.
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    password: str


app = FastAPI()
templates = Jinja2Templates(directory='templates')

# имитация бд, тестовый список
list_user = []
u1 = User(id=1, name='AA', email='ccccc', password='13344')
list_user.append(u1)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "name": "Главная"})


@app.get("/users", response_class=HTMLResponse)
async def list_users(request: Request):
    return templates.TemplateResponse('get_users_html.html', {"request": request, "name": "Список", "users": list_user})


# Task 7
# Создать RESTful API для управления списком задач. Приложение должно
# использовать FastAPI и поддерживать следующие функции:
# ○ Получение списка всех задач.
# ○ Получение информации о задаче по её ID.
# ○ Добавление новой задачи.
# ○ Обновление информации о задаче по её ID.
# ○ Удаление задачи по её ID.
# Каждая задача должна содержать следующие поля: ID (целое число),
# Название (строка), Описание (строка), Статус (строка): "todo", "in progress",
# "done".
class Task(BaseModel):
    id: int
    name_task: str
    description: str
    status: str
    is_deleted: bool


list_task = []


@app.get('/t', response_class=HTMLResponse)
async def index_task(request: Request):
    return templates.TemplateResponse('index_task.html', {'request': request, 'name': 'Главная'})


@app.get('/add-task', response_class=HTMLResponse)
async def add_task(request: Request):
    return templates.TemplateResponse('add_task.html', {'request': request, 'name': 'Добавить'})


@app.get('/update-task', response_class=HTMLResponse)
async def update(request: Request):
    return templates.TemplateResponse('update_task.html', {'request': request, 'name': 'Обновить'})


@app.get('/delete-task', response_class=HTMLResponse)
async def delete(request: Request):
    return templates.TemplateResponse('delete_task.html', {'request': request, 'name': 'Удалить'})


@app.get('/list-task', response_class=HTMLResponse)
async def get_list_task(request: Request):
    show_list = [task for task in list_task if not task.is_deleted]
    return templates.TemplateResponse('list_task.html', {'request': request, 'name': 'Удалить', 'tasks': show_list})


@app.get('/data-task', response_class=HTMLResponse)
async def get_task(request: Request):
    return templates.TemplateResponse('get_task_data.html', {'request': request, 'name': 'Сведения'})


@app.post('/data-task', response_class=HTMLResponse)
async def get_data_task(request: Request, id_task=Form()):
    id_ = int(id_task)
    return templates.TemplateResponse('data_task.html', {'request': request, 'name': 'Сведения',
                                                         'name_task': list_task[id_].name_task,
                                                         'description': list_task[id_].description,
                                                         'status': list_task[id_].status})


@app.post('/add-task', response_class=HTMLResponse)
async def add_new_task(request: Request, name_task=Form(), description=Form(), status=Form()):
    task = Task(id=len(list_task), name_task=name_task, description=description, status=status, is_deleted=False)
    list_task.append(task)
    return templates.TemplateResponse('index_task.html', {'request': request, 'name': 'Главная'})


@app.post('/update-task', response_class=HTMLResponse)
async def update_data_task(request: Request, id_task=Form(), name_task=Form(), description=Form(), status=Form()):
    id_ = int(id_task)
    list_task[id_].name_task = name_task
    list_task[id_].description = description
    list_task[id_].status = status
    return templates.TemplateResponse('index_task.html', {'request': request, 'name': 'Главная'})


@app.post('/delete-task', response_class=HTMLResponse)
async def delete_task(request: Request, id_task=Form()):
    id_ = int(id_task)
    list_task[id_].is_deleted = True
    return templates.TemplateResponse('index_task.html', {'request': request, 'name': 'Главная'})