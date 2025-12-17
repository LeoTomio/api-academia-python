from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, token_verifier
from models import User, Person, Student, Teacher
from .schema import UserSchema, LoginSchema
from main import bcrypt_context
from datetime import datetime, timedelta, timezone
from settings import settings
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter(prefix="/user", tags=["User"])


def create_token(user: User, token_duration=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    expires = datetime.now(timezone.utc) + token_duration
    # body = {"sub": str(user.id), "type": user.person.type, "exp": expires}
    body = {"sub": str(user.id), "exp": expires}
    encoded_jwt = jwt.encode(body, settings.SECRET_KEY, settings.ALGORITHM)

    return encoded_jwt


def user_autentication(cpf: str, password: str, session: Session):
    result = (
        session.query(User, Student.id.label("student_id"), Teacher.id.label("teacher_id"))
        .join(User.person)
        .outerjoin(Person.student)
        .outerjoin(Person.teacher)
        .filter(User.cpf == cpf)
        .first()
    )

    user, student_id, teacher_id = result
    if not result:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False

    user_type = None
    if teacher_id:
        user_type = "Teacher"
    elif student_id:
        user_type = "Student"

    return {"user": user, "type": user_type}


@user_router.post("/")
async def create_user(user_schema: UserSchema, session: Session = Depends(get_session)):
    """
    Rota para criar novo usuário
    """
    user = session.query(User).filter(User.cpf == user_schema.cpf).first()

    if user:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")

    new_person = Person(name=user_schema.person.name, age=user_schema.person.age, email=user_schema.person.email, phone=user_schema.person.phone)
    session.add(new_person)
    session.flush()

    hashed_password = bcrypt_context.hash(user_schema.password)
    new_user = User(cpf=user_schema.cpf, password=hashed_password, person_id=new_person.id)

    session.add(new_user)
    session.commit()

    return {"message": f"Usuário {new_user.id} cadastrado com sucesso"}


@user_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    """
    Rota para logar
    """
    user = user_autentication(login_schema.cpf, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")

    access_token = create_token(user["user"])
    refresh_token = create_token(user["user"], timedelta(days=7))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@user_router.post("/login-docs")
async def login_docs(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """
    Rota para logar no painel do fastapi
    """
    user = user_autentication(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = create_token(user["user"])

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }


@user_router.get("/refresh")
async def use_refresh_token(user: User = Depends(token_verifier)):
    """
    Rota para usar o refresh token
    """
    access_token = create_token(user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
