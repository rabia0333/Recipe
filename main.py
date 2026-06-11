from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Recipe
from schemas import RecipeCreate, RecipeResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recipe API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/recipes", response_model=RecipeResponse)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = Recipe(**recipe.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


@app.get("/recipes", response_model=list[RecipeResponse])
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Recipe).all()


@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    return recipe


@app.put("/recipes/{recipe_id}")
def update_recipe(
    recipe_id: int,
    updated: RecipeCreate,
    db: Session = Depends(get_db)
):
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    recipe.title = updated.title
    recipe.description = updated.description
    recipe.cooking_time = updated.cooking_time
    recipe.ingredient = updated.ingredient

    db.commit()

    return {"message": "Recipe updated"}


@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id
    ).first()

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Recipe not found"
        )

    db.delete(recipe)
    db.commit()

    return {"message": "Recipe deleted"}


@app.get("/search/")
def search_recipe(
    ingredient: str,
    db: Session = Depends(get_db)
):
    recipes = db.query(Recipe).filter(
        Recipe.ingredient.contains(ingredient)
    ).all()

    return recipes


from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello Recipe API"}