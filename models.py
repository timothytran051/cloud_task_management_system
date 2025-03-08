from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
Base = declarative_base()

# CREATE TABLE Task(
#     id SERIAL PRIMARY KEY,
#     title TEXT,
#     description TEXT,
#     completed BOOLEAN
# );

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    title = Column(String(255), nullable = False, index = True)
    description = Column(String(255), nullable = True)
    Completed = Column(Boolean, default = False, nullable = False)
    
    user = relationship("User", back_populates = "tasks")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, index = True, autoincrement = True)
    username = Column(String(50), unique = True, index = True, nullable = False)
    email = Column(String(255), unique = True, index = True, nullable = False)
    hashed_password = Column(String(255), nullable = False)
    
    tasks = relationship("Task", back_populates="user", cascade = "all, delete-orphan")
    