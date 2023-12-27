from fastapi import FastAPI, Depends
import models
from database import engine
from routers import auth, todos, users
from company import companyapis, dependecies

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["companysapis"],
    dependencies=[Depends(dependecies.get_token_header)],
    responses={418: {"description": "Internal use only"}}
)

