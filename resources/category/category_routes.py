from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, token_verifier
from models import Category
from .schema import CategoryCreateSchema, CategoryUpdateSchema
from sqlalchemy.orm import Session

category_router = APIRouter(prefix="/category", tags=["category"], dependencies=[Depends(token_verifier)])


@category_router.get("/")
async def category_list(session: Session = Depends(get_session)):
    """
    Rota para listar todas as categorias
    """
    categories = session.query(Category).all()
    return {"categories": categories}


@category_router.get("/{category_id}")
async def category(category_id: str, session: Session = Depends(get_session)):
    """
    Rota para selecionar uma categoria específica
    """
    category = session.query(Category).filter(Category.id == category_id).first()
    return {"categories": category}


@category_router.post("/")
async def create_category(category_schema: CategoryCreateSchema, session: Session = Depends(get_session)):
    """
    Rota para criar categoria
    """
    category = session.query(Category).filter(Category.name == category_schema.name).first()

    if category:
        raise HTTPException(status_code=400, detail="Categoria já existe")

    new_category = Category(name=category_schema.name)
    session.add(new_category)
    session.commit()
    # session.refresh(new_category) se quiser pegar o id, da pra fazer dessa forma

    return {"message": f"Categoria {new_category.name} adicionada com sucesso"}


@category_router.put("/{category_id}")
async def update_category(category_id: str, category_schema: CategoryUpdateSchema, session: Session = Depends(get_session)):
    """
    Rota para atualizar categoria
    """
    category = session.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=400, detail="Categoria não existe")
    if category_schema.name is not None:
        category.name = category_schema.name

    session.commit()

    return {"message": "Categoria atualizada com sucesso"}


@category_router.delete("/{category_id}")
async def delete_category(category_id: str, session: Session = Depends(get_session)):
    """
    Rota para deletar categoria
    """
    category = session.query(Category).filter(Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=400, detail="Categoria não existe")

    session.delete(category)
    session.commit()
    return {"message": "Categoria deletada com sucesso"}
