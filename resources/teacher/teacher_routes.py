from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, token_verifier
from models import Teacher
from .schema import TeacherCreateSchema, TeacherUpdateSchema

teacher_router = APIRouter(prefix="/teacher", tags=["Teacher"], dependencies=[Depends(token_verifier)])


@teacher_router.get("/")
async def teacher_list(session: Session = Depends(get_session)):
    """
    Rota para listar todos os professores
    """
    teachers = session.query(Teacher).all()
    return {"teachers": teachers}


@teacher_router.get("/{teacher_id}")
async def teacher(teacher_id: str, session: Session = Depends(get_session)):
    """
    Rota para pegar informações do professor
    """
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()

    if not teacher:
        raise HTTPException(status_code=400, detail="Professor não existe")

    return {"teacher": teacher}


@teacher_router.post("/")
async def create_teacher(teacherCreateSchema: TeacherCreateSchema, session: Session = Depends(get_session)):
    """
    Rota para adicionar um professor
    """
    teacher = session.query(Teacher).filter(Teacher.cref == teacherCreateSchema.cref).first()

    if teacher:
        raise HTTPException(status_code=400, detail="Professor já existe")

    new_teacher = Teacher(cref=teacherCreateSchema.cref, person_id=teacherCreateSchema.person_id)
    session.add(new_teacher)
    session.commit()

    return {"message": f"Professor {new_teacher.cref} criado com sucesso"}


@teacher_router.put("/")
async def update_teacher(teacherUpdateSchema: TeacherUpdateSchema, session: Session = Depends(get_session)):
    """
    Rota para editar um professor
    """
    teacher = session.query(Teacher).filter(Teacher.cref == teacherUpdateSchema.cref).first()

    if not teacher:
        raise HTTPException(status_code=400, detail="Professor não existe")

    update_data = teacherUpdateSchema.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(teacher, field, value)

    session.commit()

    return {"message": "Professor atualizado com sucesso"}


@teacher_router.delete("/{teacher_id}")
async def delete_teacher(teacher_id: str, session: Session = Depends(get_session)):
    """
    Rota para deletar um professor
    """
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()

    if not teacher:
        raise HTTPException(status_code=400, detail="Professor não existe")

    session.delete(teacher)
    session.commit()

    return {"message": "Professor deletado com sucesso"}
