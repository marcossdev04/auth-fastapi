from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.connection import Session as DatabaseSession
from app.auth_user import UserUseCases

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_db_session():
    try:
        session = DatabaseSession()
        yield session
    finally:
        session.close()

def token_verifier(
    db_session: Session = Depends(get_db_session),
    token = Depends(oauth_scheme)
):
    try:
        uc = UserUseCases(db_session=db_session)
        uc.verify_token(access_token=token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )