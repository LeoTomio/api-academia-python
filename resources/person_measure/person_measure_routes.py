from fastapi import APIRouter, Depends, HTTPException
from dependencies import token_verifier, get_session
from sqlalchemy.orm import Session
from .schema import PersonMeasureCreateSchema, PersonMeasureUpdateSchema
from models import PersonMeasure

person_measure_router = APIRouter(prefix="/measure", tags=["Measure"], dependencies=[Depends(token_verifier)])


@person_measure_router.get("/{person_id}")
async def person_measure_list(person_id: str, session: Session = Depends(get_session)):
    """
    Rota para listar todas as medidas do aluno
    """
    person_measures = session.query(PersonMeasure).filter(PersonMeasure.person_id == person_id).all()
    return {"measures": person_measures}


@person_measure_router.post("/")
async def create_person_measure(person_measure_schema: PersonMeasureCreateSchema, session: Session = Depends(get_session)):
    """
    Rota para adicionar medida do aluno
    """
    person_measure = session.query(PersonMeasure).filter(PersonMeasure.measure_id == person_measure_schema.measure_id).first()

    if person_measure:
        raise HTTPException(status_code=400, detail="Aluno já possui esta medida")

    new_person_measure = PersonMeasure(measure_id=person_measure_schema.measure_id, unit=person_measure_schema.value)
    session.add(new_person_measure)
    session.commit()

    return {"message": "Medida adicionada com sucesso"}


@person_measure_router.put("/{person_measure_id}")
async def update_person_measure(person_measure_id: str, person_measure_schema: PersonMeasureUpdateSchema, session: Session = Depends(get_session)):
    """
    Rota para atualizar medida de aluno
    """
    person_measure = session.query(PersonMeasure).filter(PersonMeasure.id == person_measure_id).first()

    if not person_measure:
        raise HTTPException(status_code=400, detail="Aluno não possui esta medida")

    update_data = person_measure_schema.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(person_measure, field, value)
    session.commit()

    return {"message": "Medida atualizada com sucesso"}


@person_measure_router.delete("/{person_measure_id}")
async def delete_person_measure(person_measure_id: str, session: Session = Depends(get_session)):
    """
    Rota para deletar medida do aluno
    """
    person_measure = session.query(PersonMeasure).filter(PersonMeasure.id == person_measure_id).first()

    if not person_measure:
        raise HTTPException(status_code=400, detail="Medida não existe")

    session.delete(person_measure)
    session.commit()
    return {"message": "Medida deletada com sucesso"}
