from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="user/login-docs")

from resources.category.category_routes import category_router
from resources.exercise.exercise_routes import exercise_router
from resources.measure.measure_routes import measure_router
from resources.person.person_routes import person_router
from resources.plan.plan_routes import plan_router
from resources.student.student_routes import student_router
from resources.teacher.teacher_routes import teacher_router
from resources.training_plan.training_plan_routes import training_plan_router
from resources.training.training_routes import training_router
from resources.user.user_routes import user_router

app.include_router(category_router)
app.include_router(exercise_router)
app.include_router(measure_router)
app.include_router(person_router)
app.include_router(plan_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(training_plan_router)
app.include_router(training_router)
app.include_router(user_router)
