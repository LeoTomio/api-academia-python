import uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID

# Conexão de banco
db = create_engine("postgresql+psycopg2://postgres:root@localhost:5432/academyDb")

Base = declarative_base()


# ----------------------- PLAN -----------------------
class Plan(Base):
    __tablename__ = "plan"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column("name", String, unique=True, nullable=False)
    price = Column("price", Float, default=0.00)
    description = Column("description", String)
    duration_months = Column("duration_months", Integer, nullable=False)

    persons = relationship("Person", back_populates="plan")


# ----------------------- PERSON -----------------------
class Person(Base):
    __tablename__ = "person"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column("name", String, nullable=False)
    age = Column("age", Integer)
    phone = Column("phone", String)
    email = Column("email", String)
    is_active = Column("is_active", Boolean, default=True)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plan.id", ondelete="SET NULL"), nullable=True)

    # Relacionamentos
    user = relationship("User", back_populates="person", uselist=False)
    teacher = relationship("Teacher", back_populates="person", uselist=False)
    student = relationship("Student", back_populates="person", uselist=False)

    measures = relationship("PersonMeasure", back_populates="person")  # 1:N
    trainings = relationship("Training", back_populates="person")  # 1:N
    plan = relationship("Plan", back_populates="persons")  # 1:N


# ------------------------ USER -------------------------


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    cpf = Column("cpf", String, unique=True, nullable=False)
    password = Column("password", String, nullable=False)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id", ondelete="CASCADE"), nullable=False)

    # Relacionamentos
    person = relationship("Person", back_populates="user")


# ----------------------- TEACHER -----------------------
class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id", ondelete="CASCADE"), nullable=False)
    cref = Column("cref", String, nullable=False)

    # Relacionamentos
    person = relationship("Person", back_populates="teacher")
    students = relationship("Student", back_populates="teacher", uselist=True)


# ----------------------- STUDENT -----------------------
class Student(Base):
    __tablename__ = "student"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    registration_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    objective = Column("objective", String)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id", ondelete="CASCADE"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teacher.id"))

    # Relacionamentos
    person = relationship("Person", back_populates="student")
    teacher = relationship("Teacher", back_populates="students")


# ----------------------- MEASURE -----------------------
class PersonMeasure(Base):
    __tablename__ = "person_measure"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    measure_id = Column(UUID(as_uuid=True), ForeignKey("measure.id", ondelete="CASCADE"), nullable=False)
    value = Column("value", Float)
    date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id", ondelete="CASCADE"), nullable=False)

    # Relacionamentos
    measure = relationship("Measure", back_populates="person_measures")
    person = relationship("Person", back_populates="measures")


# -------------------- PERSON MEASURE --------------------


class Measure(Base):
    __tablename__ = "measure"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column("name", String, unique=True, nullable=False)
    unit = Column("unit", String, nullable=False)

    # Relacionamentos
    person_measures = relationship("PersonMeasure", back_populates="measure", cascade="all, delete-orphan")


# ----------------------- CATEGORY -----------------------
class Category(Base):
    __tablename__ = "category"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column("name", String, unique=True, nullable=False)

    # Relacionamentos
    exercises = relationship("Exercise", back_populates="category")


# ----------------------- EXERCISE -----------------------
class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column("name", String, unique=True, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("category.id", ondelete="CASCADE"), nullable=False)

    # Relacionamentos
    category = relationship("Category", back_populates="exercises")
    training_plans = relationship("TrainingPlan", back_populates="exercise")


# ----------------------- TRAINING -----------------------
class Training(Base):
    __tablename__ = "training"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column("name", String, nullable=False)
    person_id = Column(UUID(as_uuid=True), ForeignKey("person.id", ondelete="CASCADE"), nullable=False)

    # Relacionamentos
    person = relationship("Person", back_populates="trainings")
    training_plans = relationship("TrainingPlan", back_populates="training")


# ----------------------- TRAINING PLAN -----------------------
class TrainingPlan(Base):
    __tablename__ = "training_plan"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    training_id = Column(UUID(as_uuid=True), ForeignKey("training.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(UUID(as_uuid=True), ForeignKey("exercise.id", ondelete="CASCADE"), nullable=False)
    repetitions = Column("repetitions", Integer, nullable=False)

    # Relacionamentos
    training = relationship("Training", back_populates="training_plans")
    exercise = relationship("Exercise", back_populates="training_plans")

    __table_args__ = (
        UniqueConstraint("training_id", "exercise_id", name="uq_training_exercise"),
    )