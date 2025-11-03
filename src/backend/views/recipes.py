import os
from fastapi import APIRouter, Depends, Body, HTTPException
from starlette.responses import JSONResponse, FileResponse

from src.backend.lib.auth import get_current_user, require_admin
from src.backend.lib.database import db, row_to_dict, rows_to_dict_list

router = APIRouter(prefix="/recipes", tags=["recipes"])



@router.get("/static")
async def get_static_recipes(file_name: str):
    print(file_name)
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    file_path = os.path.abspath(os.path.join(static_dir, file_name))
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


@router.get("/static/list")
async def list_static_recipes():
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    files = []
    for file_name in os.listdir(static_dir):
        file_path = os.path.abspath(os.path.join(static_dir, file_name))
        if os.path.isfile(file_path):
            files.append(file_name)
    return {"files": files}

@router.post("/")
async def create_recipe(
    title: str = Body("title"),
    content: str = Body("content"),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new recipe (requires authentication).

    Args:
        title: Recipe title
        content: Recipe content/instructions
        current_user: Current authenticated user (from JWT)

    Returns:
        Success message
    """
    try:
        user_id = current_user.get("user_id")
        query = f"INSERT INTO recipes (user_id, title, content) VALUES ({user_id}, '{title}', '{content}')"
        db.execute(query)
        return {
            "message": "Recipe created successfully",
            "author": current_user.get("username")
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@router.get("/{recipe_id}")
async def get_recipe(recipe_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get a specific recipe by ID (requires authentication).

    Args:
        recipe_id: Recipe ID
        current_user: Current authenticated user

    Returns:
        Recipe information
    """
    try:
        query = f"""
            SELECT recipes.id, recipes.title, recipes.content,
                   recipes.created_at, users.username as author, users.id as author_id
            FROM recipes
            JOIN users ON recipes.user_id = users.id
            WHERE recipes.id = {recipe_id}
        """
        row = db.fetch_one(query)
        if row:
            recipe = row_to_dict(row)
            return {"recipe": recipe}
        return JSONResponse(
            status_code=404,
            content={"error": "Recipe not found"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@router.delete("/{recipe_id}")
async def delete_recipe(recipe_id: str, current_user: dict = Depends(require_admin)):
    """
    Delete a recipe (admin only).

    Args:
        recipe_id: Recipe ID to delete
        current_user: Current authenticated admin user

    Returns:
        Success message
    """
    try:
        query = f"DELETE FROM recipes WHERE id = {recipe_id}"
        db.execute(query)
        return {
            "message": "Recipe deleted successfully",
            "deleted_by": current_user.get("username")
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )



@router.get("/")
async def get_recipes(current_user: dict = Depends(get_current_user)):
    """
    Get all recipes (requires authentication).

    Returns:
        List of all recipes with author information
    """
    try:
        query = """
            SELECT recipes.id, recipes.title, recipes.content,
                   recipes.created_at, users.username as author
            FROM recipes
            JOIN users ON recipes.user_id = users.id
        """
        rows = db.fetch_all(query)
        recipes = rows_to_dict_list(rows)
        return {
            "recipes": recipes,
            "authenticated_as": current_user.get("username")
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
