# JSON web token = jwt
# swagger = localhost /doc
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import User

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


# генерация токена - шифрование
def create_access_token(data: User, expires_minutes: int):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    # data.update({"exp": expire})
    encoded_jwt = jwt.encode(data.model_dump(), SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# проверка токена - дешифрование
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    return payload