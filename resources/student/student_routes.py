from fastapi import APIRouter, Depends, HTTPException
from dependencies import token_verifier, get_session
from models import Student
from .schema import StudentCreateSchema, StudentUpdateSchema
from sqlalchemy.orm import Session

student_router = APIRouter(prefix="/student", tags=["Student"], dependencies=[Depends(token_verifier)])


@student_router.get("/")
async def student_list(teacher_id: str, session: Session = Depends(get_session)):
    """
    Rota para listar todos os alunos
    """
    query = session.query(Student)

    if teacher_id:
        query = query.filter(Student.teacher_id == teacher_id)

    students = query.all()

    students = session.query(Student).all()
    return {"students": students}


@student_router.get("/{student_id}")
async def student(student_id: str, session: Session = Depends(get_session)):
    """
    Rota para selecionar um aluno específico
    """
    student = session.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=400, detail="Aluno não existe")

    return {"student": student}


@student_router.post("/")
async def create_student(student_schema: StudentCreateSchema, session: Session = Depends(get_session)):
    """
    Rota para criar aluno
    """
    student = session.query(Student).filter(Student.person_id == student_schema.person_id).first()

    if student:
        raise HTTPException(status_code=400, detail="Aluno já existe")

    new_student = Student(
        objective=student_schema.objective,
        person_id=student_schema.person_id,
        teacher_id=student_schema.teacher_id,
    )
    session.add(new_student)
    session.commit()

    return {"message": "Aluno adicionado com sucesso"}


@student_router.put("/{student_id}")
async def update_student(student_id: str, student_schema: StudentUpdateSchema, session: Session = Depends(get_session)):
    """
    Rota para atualizar aluno
    """
    student = session.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=400, detail="Aluno não existe")

    update_data = student_schema.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(student, field, value)

    session.commit()

    return {"message": "Aluno atualizado com sucesso"}
