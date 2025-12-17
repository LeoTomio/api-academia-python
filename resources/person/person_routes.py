from fastapi import APIRouter, Depends, HTTPException
from dependencies import token_verifier, get_session
from models import Person
from .schema import PersonCreateSchema, PersonUpdateSchema 
from sqlalchemy.orm import Session, joinedload
from utils.serializers import to_dict

person_router = APIRouter(prefix="/person", tags=["Person"], dependencies=[Depends(token_verifier)])


@person_router.get("/")
async def person_list(session: Session = Depends(get_session)):
    """
    Rota para listar todas as pessoas
    """
    persons = session.query(Person).all()
    return {"persons": persons}


@person_router.get("/{person_id}")
async def person(person_id: str, session: Session = Depends(get_session)):
    """
    Rota para selecionar uma pessoa específica
    """
    person = session.query(Person).options(joinedload(Person.student), joinedload(Person.teacher)).filter(Person.id == person_id).first()

    if not person:
        raise HTTPException(status_code=400, detail="Pessoa não existe")

    return {"person": to_dict(person), "student": to_dict(person.student), "teacher": to_dict(person.teacher)}


@person_router.post("/")
async def create_person(person_schema: PersonCreateSchema, session: Session = Depends(get_session)):
    """
    Rota para criar pessoa
    """
    person = session.query(Person).filter(Person.name == person_schema.name).first()

    if person:
        raise HTTPException(status_code=400, detail="Pessoa já existe")

    new_person = Person(name=person_schema.name)
    session.add(new_person)
    session.commit()

    return {"message": f"Pessoa {new_person.name} adicionada com sucesso"}


@person_router.put("/{person_id}")
async def update_person(person_id: str, person_schema: PersonUpdateSchema, session: Session = Depends(get_session)):
    """
    Rota para atualizar pessoa
    """
    person = session.query(Person).filter(Person.id == person_id).first()

    if not person:
        raise HTTPException(status_code=400, detail="Pessoa não existe")
    if person_schema.name is not None:
        person.name = person_schema.name

    session.commit()

    return {"message": "Pessoa atualizada com sucesso"}


@person_router.delete("/{person_id}")
async def delete_person(person_id: str, session: Session = Depends(get_session)):
    """
    Rota para deletar pessoa
    """
    person = session.query(Person).filter(Person.id == person_id).first()

    if not person:
        raise HTTPException(status_code=400, detail="Pessoa não existe")

    session.delete(person)
    session.commit()
    return {"message": "Pessoa deletada com sucesso"}
