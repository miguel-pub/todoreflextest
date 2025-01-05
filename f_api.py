from typing import Annotated, Type
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    entry: str = Field(index=True)
    priority: int | None = Field(default=1, index=True)

sqlite_file_name = "todoreflextest/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()#

@app.post("/todos/")
def create_todo(todo: Todo, session: SessionDep) -> Todo:
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@app.get("/todos/{entry_id}")
def read_entry(entry_id: int, session: SessionDep) -> Todo:
    entry = session.get(Todo, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Todo not found")
    return entry
