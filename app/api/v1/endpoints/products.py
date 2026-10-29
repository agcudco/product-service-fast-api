from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID
from app.api.deps import get_db
from app.crud.product import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product,
)
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(
    payload: ProductCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_product(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese SKU")


@router.get("/", response_model=list[ProductRead])
def list_products_endpoint(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * limit
    return get_products(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product_endpoint(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    db_obj = get_product(db, product_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_obj


@router.patch("/{product_id}", response_model=ProductRead)
def update_product_endpoint(
    product_id: UUID,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
):
    db_obj = get_product(db, product_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    try:
        return update_product(db, db_obj, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Conflicto al actualizar producto")


@router.delete("/{product_id}", response_model=ProductRead)
def delete_product_endpoint(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    db_obj = get_product(db, product_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return delete_product(db, db_obj)