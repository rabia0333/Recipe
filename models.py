from sqlalchemy import Column, Integer, String
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    cooking_time = Column(Integer)
    ingredient = Column(String)