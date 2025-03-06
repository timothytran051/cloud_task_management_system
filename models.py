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
    user_id = Column(Integer, ForiegnKey("users.id"), nullable = False)
    title = Column(String(255), nullable = False, index = True)
    description = Column(String(255), nullable = True)
    Completed = Column(Boolean, default = False, nullable = False)
    
    user = relationship("User", back_populates = "tasks")