from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, token_verifier
from models import Plan
from .schema import PlanCreateSchema, PlanUpdateSchema
from sqlalchemy.orm import Session

plan_router = APIRouter(prefix="/plan", tags=["plan"], dependencies=[Depends(token_verifier)])


@plan_router.get("/")
async def plan_list(session: Session = Depends(get_session)):
    """
    Rota para listar planos
    """
    plans = session.query(Plan).all()
    return {"plans": plans}


@plan_router.get("/{plan_id}")
async def plan(plan_id: str, session: Session = Depends(get_session)):
    """
    Rota para selecionar um plano específico
    """
    plan = session.query(Plan).filter(Plan.id == plan_id).first()
    return {"plans": plan}


@plan_router.post("/")
async def create_plan(plan_schema: PlanCreateSchema, session: Session = Depends(get_session)):
    """
    Rota para criar um plano
    """
    plan = session.query(Plan).filter(Plan.name == plan_schema.name).first()

    if plan:
        raise HTTPException(status_code=400, detail="Plano já existe")

    new_plan = Plan(name=plan_schema.name, price=plan_schema.price, description=plan_schema.description, duration_months=plan_schema.duration_months)
    session.add(new_plan)
    session.commit()

    return {"message": f"Plano {new_plan.name} adicionado com sucesso"}


@plan_router.put("/{plan_id}")
async def update_plan(plan_id: str, plan_schema: PlanUpdateSchema, session: Session = Depends(get_session)):
    """
    Rota para atualizar um plano
    """
    plan = session.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        raise HTTPException(status_code=400, detail="Plano não existe")

    update_data = plan_schema.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(plan, field, value)

    session.commit()

    return {"message": "Plano atualizado com sucesso"}


@plan_router.delete("/{plan_id}")
async def delete_plan(plan_id: str, session: Session = Depends(get_session)):
    """
    Rota para deletar um plano
    """
    plan = session.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        raise HTTPException(status_code=400, detail="Plano não existe")

    session.delete(plan)
    session.commit()
    return {"message": "Plano deletada com sucesso"}
