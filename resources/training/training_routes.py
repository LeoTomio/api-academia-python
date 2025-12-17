from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Training
from dependencies import token_verifier, get_session
from .schema import TrainingCreateSchema, TrainingUpdateSchema

training_router = APIRouter(prefix="/training", tags=["Training"], dependencies=[Depends(token_verifier)])

@training_router.get("/{person_id}")
async def training_list(person_id: str, session: Session = Depends(get_session)):
    """
    Rota para listar todas os treinos do aluno
    """
    training = session.query(Training).filter(Training.person_id == person_id).all()
    return {"training": training}


@training_router.post("/")
async def create_training(training_schema: TrainingCreateSchema, session: Session = Depends(get_session)):
    """
    Rota para adicionar treinos para o aluno
    """
    training = session.query(Training).filter(Training.name == training_schema.name).first()

    if training:
        raise HTTPException(status_code=400, detail="Aluno já possui este treino")

    new_training = Training(name=training_schema.name, person_id=training_schema.person_id)
    session.add(new_training)
    session.commit()

    return {"message": f"Treino {new_training.name} adicionado com sucesso"}


@training_router.put("/{training_id}")
async def update_training(training_id: str, training_schema: TrainingUpdateSchema, session: Session = Depends(get_session)):
    """
    Rota para atualizar treino do aluno
    """
    training = session.query(Training).filter(Training.id == training_id).first()

    if not training:
        raise HTTPException(status_code=400, detail="Aluno não possui este treino")

    update_data = training_schema.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(training, field, value)
    session.commit()

    return {"message": "Treino atualizado com sucesso"}


@training_router.delete("/{training_id}")
async def delete_training(training_id: str, session: Session = Depends(get_session)):
    """
    Rota para deletar treino do aluno
    """
    training = session.query(Training).filter(Training.id == training_id).first()

    if not training:
        raise HTTPException(status_code=400, detail="Treino não existe")

    session.delete(training)
    session.commit()
    return {"message": "Treino deletado com sucesso"}
