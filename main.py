from fastapi import FastAPI, Depends

from security import create_access_token, get_current_user
from schemas import User

app = FastAPI()


# Незащищенный маршрут
@app.get('/users')
async def get_all_users():
    users = {'pasha', 'misha', 'mikle'}

    return {'all_users': users}


#регистрация
@app.post('/register')
async def register_user(user_data: User):
    current_user_jwt = create_access_token(user_data, 30)

    return current_user_jwt


#опубликавать пост
@app.post('/public-post')
async def new_post(post_header: str, post_comment: str, user_jwt=Depends(get_current_user)):
    return {'расшифрованные данные': user_jwt}

