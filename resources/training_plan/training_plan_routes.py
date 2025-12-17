from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import token_verifier, get_session
from .schema import TrainingPlanUpdateSchema, TrainingPlanCreateSchema
from models import TrainingPlan

training_plan_router = APIRouter(prefix="/training_plan", tags=["Training_plan"], dependencies=[Depends(token_verifier)])


@training_plan_router.get("/{training_id}")
async def training_plan_list(training_id: str, session: Session = Depends(get_session)):
    """
    Rota para listar todos os exercícios do treino
    """
    training_plan = session.query(TrainingPlan).filter(TrainingPlan.training_id == training_id).all()
    return {"training_plan": training_plan}


@training_plan_router.post("/")
async def create_training_plan(training_plan_schema: TrainingPlanCreateSchema, session: Session = Depends(get_session)):
    """
    Rota para adicionar exercícios ao treino
    """
    training_plan = (
        session.query(TrainingPlan)
        .filter(TrainingPlan.training_id == training_plan_schema.training_id, TrainingPlan.exercise_id == training_plan_schema.exercise_id)
        .first()
    )

    if training_plan:
        raise HTTPException(status_code=400, detail="Esse treino ja possui este exercício")

    new_training_plan = TrainingPlan(
        training_id=training_plan_schema.training_id, exercise_id=training_plan_schema.exercise_id, repetitions=training_plan_schema.repetitions
    )
    session.add(new_training_plan)
    session.commit()

    return {"message": "Exercício adicionado ao treino com sucesso"}


@training_plan_router.put("/{training_plan_id}")
async def update_training_plan(training_plan_id: str, training_plan_schema: TrainingPlanUpdateSchema, session: Session = Depends(get_session)):
    """
    Rota para atualizar exercício do treino
    """
    training_plan = session.query(TrainingPlan).filter(TrainingPlan.id == training_plan_id).first()

    if not training_plan:
        raise HTTPException(status_code=400, detail="Exercício não existe nesse treino")

    update_data = training_plan_schema.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(training_plan, field, value)
    session.commit()

    return {"message": "Exercício atualizado com sucesso"}


@training_plan_router.delete("/{training_plan_id}")
async def delete_training_plan(training_plan_id: str, session: Session = Depends(get_session)):
    """
    Rota para deletar exercício do treino
    """
    training_plan = session.query(TrainingPlan).filter(TrainingPlan.id == training_plan_id).first()

    if not training_plan:
        raise HTTPException(status_code=400, detail="Exercício não existe nesse treino")

    session.delete(training_plan)
    session.commit()
    return {"message": "Exercício deletado com sucesso"}
