from pydantic import BaseModel

class RecipeCreate(BaseModel):
    title: str
    description: str
    cooking_time: int
    ingredient: str


class RecipeResponse(RecipeCreate):
    id: int

    class Config:
        from_attributes = True