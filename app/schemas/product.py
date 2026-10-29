from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    sku: str = Field(min_length=2, max_length=50)
    nombre: str = Field(min_length=2, max_length=150)
    descripcion: str | None = Field(default=None, max_length=1000)
    marca: str | None = Field(default=None, max_length=100)
    precio_venta: Decimal = Field(gt=0)
    stock: int = Field(ge=0)
    stock_minimo: int = Field(ge=0)
    estado: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    sku: str | None = Field(default=None, min_length=2, max_length=50)
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    descripcion: str | None = Field(default=None, max_length=1000)
    marca: str | None = Field(default=None, max_length=100)
    precio_venta: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    stock_minimo: int | None = Field(default=None, ge=0)
    estado: bool | None = None


class ProductRead(ProductBase):
    id: UUID
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    fecha_eliminacion: datetime | None = None

    model_config = ConfigDict(from_attributes=True)