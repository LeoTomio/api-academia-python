from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from models import db, User
from main import oauth2_schema
from settings import settings
from jose import jwt, JWTError


def get_session():
    try:
        Session = sessionmaker(db)
        session = Session()
        yield session
    finally:
        session.close()


def token_verifier(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        user_id = str(decoded_token.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Inválido")

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Acesso Inválido")

    return user
