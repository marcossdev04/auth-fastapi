from sqlalchemy.orm import Session
from app.db.models import UserModel
from app.schemas import User
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
crypt_context = CryptContext(schemes=["sha256_crypt"],)


class UserUseCases:
    def __init__( self, db_session: Session):
        self.db_session = db_session

    def user_register(self, user:User):
        user_model = UserModel(
            username = user.username,
            password = crypt_context.hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
    def user_login(self,user:User,expires_in:int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(username = user.username).first()

        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        if not crypt_context.verify(user.password, user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        exp = datetime.now() + timedelta(minutes=expires_in)

        payload = {
            "sub": user.username,
            "exp": exp
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "access_token": token,
            "exp" : exp.isoformat()
        }