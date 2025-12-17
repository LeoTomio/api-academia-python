from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, token_verifier
from models import Exercise
from .schema import ExerciseCreateSchema, ExerciseUpdateSchema
from sqlalchemy.orm import Session

exercise_router = APIRouter(prefix="/exercise", tags=["Exercise"], dependencies=[Depends(token_verifier)])


@exercise_router.get("/")
async def exercise_list(session: Session = Depends(get_session)):
    """
    Rota para listar exercícios
    """
    exercises = session.query(Exercise).all()
    return {"exercises": exercises}


@exercise_router.get("/{exercise_id}")
async def exercise(exercise_id: str, session: Session = Depends(get_session)):
    """
    Rota para selecionar um exercício específico
    """
    exercise = session.query(Exercise).filter(Exercise.id == exercise_id).first()
    return {"exercises": exercise}


@exercise_router.get("/lista/{category_id}")
async def exercise(category_id: str, session: Session = Depends(get_session)):
    """
    Rota para listar todos os exercícios de uma categoria
    """
    exercises = session.query(Exercise).filter(Exercise.category_id == category_id).all()
    return {"exercises": exercises}


@exercise_router.post("/")
async def create_exercise(exercise_schema: ExerciseCreateSchema, session: Session = Depends(get_session)):
    """
    Rota para criar um exercício
    """
    exercise = session.query(Exercise).filter(Exercise.name == exercise_schema.name).first()

    if exercise:
        raise HTTPException(status_code=400, detail="Exercício já existe")

    new_exercise = Exercise(
        name=exercise_schema.name,
        category_id=exercise_schema.category_id,
    )
    session.add(new_exercise)
    session.commit()

    return {"message": f"Exercício {new_exercise.name} adicionado com sucesso"}


@exercise_router.put("/{exercise_id}")
async def update_exercise(exercise_id: str, exercise_schema: ExerciseUpdateSchema, session: Session = Depends(get_session)):
    """
    Rota para atualizar um exercício
    """
    exercise = session.query(Exercise).filter(Exercise.id == exercise_id).first()

    if not exercise:
        raise HTTPException(status_code=400, detail="Exercício não existe")

    update_data = exercise_schema.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(exercise, field, value)

    session.commit()

    return {"message": "Exercício atualizado com sucesso"}


@exercise_router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: str, session: Session = Depends(get_session)):
    """
    Rota para deletar um exercício
    """
    exercise = session.query(Exercise).filter(Exercise.id == exercise_id).first()

    if not exercise:
        raise HTTPException(status_code=400, detail="Exercício não existe")

    session.delete(exercise)
    session.commit()
    return {"message": "Exercício deletada com sucesso"}
