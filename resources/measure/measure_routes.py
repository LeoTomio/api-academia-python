from fastapi import APIRouter, Depends, HTTPException
from dependencies import token_verifier, get_session
from sqlalchemy.orm import Session
from .schema import MeasureCreateSchema, MeasureUpdateSchema
from models import Measure

measure_router = APIRouter(prefix="/measure", tags=["Measure"], dependencies=[Depends(token_verifier)])


@measure_router.get("/")
async def measure_list(session: Session = Depends(get_session)):
    """
    Rota para listar todas as medidas
    """
    measures = session.query(Measure).all()
    return {"measures": measures}

@measure_router.get("/{measure_id}")
async def category(measure_id: str, session: Session = Depends(get_session)):
    """
    Rota para selecionar uma medidas específica
    """
    measure = session.query(Measure).filter(Measure.id == measure_id).first()
    
    if not measure:
        raise HTTPException(status_code=400, detail="Medida não existe")
    
    return {"measures": measure}


@measure_router.post("/")
async def create_measure(measure_schema: MeasureCreateSchema, session: Session = Depends(get_session)):
    """
    Rota para criar medida
    """
    measure = session.query(Measure).filter(Measure.name == measure_schema.name).first()

    if measure:
        raise HTTPException(status_code=400, detail="Medida já existe")

    new_measure = Measure(name=measure_schema.name, unit=measure_schema.unit)
    session.add(new_measure)
    session.commit() 

    return {"message": f"Medida '{new_measure.name}' adicionada com sucesso"}


@measure_router.put("/{measure_id}")
async def update_measure(measure_id: str, measure_schema: MeasureUpdateSchema, session: Session = Depends(get_session)):
    """
    Rota para atualizar medida
    """
    measure = session.query(Measure).filter(Measure.id == measure_id).first()

    if not measure:
        raise HTTPException(status_code=400, detail="Medida não existe")
   
    update_data = measure_schema.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(measure, field, value)

    session.commit()

    return {"message": "Medida atualizada com sucesso"}


@measure_router.delete("/{measure_id}")
async def delete_measure(measure_id: str, session: Session = Depends(get_session)):
    """
    Rota para deletar medida
    """
    measure = session.query(Measure).filter(Measure.id == measure_id).first()

    if not measure:
        raise HTTPException(status_code=400, detail="Medida não existe")

    session.delete(measure)
    session.commit()
    return {"message": "Medida deletada com sucesso"}
