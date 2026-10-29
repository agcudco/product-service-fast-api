from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db
from app.crud.category import (
    create_category,
    delete_category,
    get_categories,
    get_category,
    update_category,
)
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category_endpoint(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_category(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe una categoría con ese código")


@router.get("/", response_model=list[CategoryRead])
def list_categories_endpoint(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * limit
    return get_categories(db, skip=skip, limit=limit)


@router.get("/{category_id}", response_model=CategoryRead)
def get_category_endpoint(
    category_id: UUID,
    db: Session = Depends(get_db),
):
    db_obj = get_category(db, category_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_obj


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category_endpoint(
    category_id: UUID,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
):
    db_obj = get_category(db, category_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    try:
        return update_category(db, db_obj, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflicto al actualizar categoría")


@router.delete("/{category_id}", response_model=CategoryRead)
def delete_category_endpoint(
    category_id: UUID,
    db: Session = Depends(get_db),
):
    db_obj = get_category(db, category_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    return delete_category(db, db_obj)