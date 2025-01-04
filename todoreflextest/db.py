from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

DATABASE_URL = "sqlite:///db.sqlite"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    priority = Column(Integer, nullable=False, default=1)



    def __repr__(self):
         return f"Todo(id={self.id}, title='{self.title}', priority={self.priority})"
    
def init_db():
     Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
     init_db()