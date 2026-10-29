from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_db
from app.crud.category import get_category
from app.crud.product import get_product
from app.crud.product_category import (
    create_product_category,
    delete_product_category,
    get_categories_by_product,
    get_product_categories,
    get_product_category,
    get_products_by_category,
    update_product_category,
)
from app.schemas.product_category import (
    ProductCategoryCreate,
    ProductCategoryRead,
    ProductCategoryUpdate,
)

router = APIRouter(prefix="/product-categories", tags=["Product Categories"])


@router.post("/", response_model=ProductCategoryRead, status_code=status.HTTP_201_CREATED)
def create_product_category_endpoint(
    payload: ProductCategoryCreate,
    db: Session = Depends(get_db),
):
    product = get_product(db, payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    category = get_category(db, payload.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    try:
        return create_product_category(db, payload)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="La relación producto-categoría ya existe",
        )


@router.get("/", response_model=list[ProductCategoryRead])
def list_product_categories_endpoint(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * limit
    return get_product_categories(db, skip=skip, limit=limit)


@router.get("/by-product/{product_id}", response_model=list[ProductCategoryRead])
def get_categories_of_product_endpoint(
    product_id: UUID,
    db: Session = Depends(get_db),
):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return get_categories_by_product(db, product_id)


@router.get("/by-category/{category_id}", response_model=list[ProductCategoryRead])
def get_products_of_category_endpoint(
    category_id: str,
    db: Session = Depends(get_db),
):
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    return get_products_by_category(db, category_id)


@router.get("/{relation_id}", response_model=ProductCategoryRead)
def get_product_category_endpoint(
    relation_id: UUID,
    db: Session = Depends(get_db),
):
    db_obj = get_product_category(db, relation_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    return db_obj


@router.patch("/{relation_id}", response_model=ProductCategoryRead)
def update_product_category_endpoint(
    relation_id: UUID,
    payload: ProductCategoryUpdate,
    db: Session = Depends(get_db),
):
    db_obj = get_product_category(db, relation_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Relación no encontrada")

    return update_product_category(db, db_obj, payload)


@router.delete("/{relation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_category_endpoint(
    relation_id: UUID,
    db: Session = Depends(get_db),
):
    db_obj = get_product_category(db, relation_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Relación no encontrada")

    delete_product_category(db, db_obj)
    return None