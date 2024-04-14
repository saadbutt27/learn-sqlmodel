from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import SQLModel, Session, select
from app.db import engine
from app.models import Hero
from contextlib import asynccontextmanager

def create_db_tables():
    print("creating tables")
    SQLModel.metadata.create_all(engine)
    print("done")

@asynccontextmanager
async def life_span(app_db: FastAPI):
    print("Server startup")
    create_db_tables()
    yield 


app_db:FastAPI = FastAPI(lifespan=life_span)

def get_session():
    with Session(engine) as session:
        yield session

@app_db.post("/heroes")
def create_heroes(hero_data: Hero, session:Annotated[Session, Depends(get_session)]):
    session.add(hero_data)
    session.commit()
    session.refresh(hero_data)
    return hero_data
    
@app_db.get("/heroes")
def get_all_heroes(session:Annotated[Session, Depends(get_session)]):
        query = select(Hero)
        all_heroes = session.exec(query).all()
        return all_heroes

@app_db.get("/hero/{hero_id}")
def get_todo(hero_id:int, session:Annotated[Session, Depends(get_session)]):
        query = select(Hero).where(Hero.id == hero_id)
        hero = session.exec(query).all()
        return hero
