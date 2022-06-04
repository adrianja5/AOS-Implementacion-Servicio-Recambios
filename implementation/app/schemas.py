from typing import TypedDict, Union

from pydantic import BaseModel, Field


# Schema genérico
class Dimensiones(BaseModel):
  alto: float = Field(ge=0, default=0)
  ancho: float = Field(ge=0, default=0)
  largo: float = Field(ge=0, default=0)


# Schemas de recambios
class RecambioBase(BaseModel):
  nombre: str
  descripcion: Union[str, None] = None
  proveedor: str
  modelo: str
  cantidad: int = Field(ge=0)
  vehiculos_compatibles: Union[list[str], None] = None
  peso: Union[float, None] = Field(None, gt=0)
  dimensiones: Union[Dimensiones, None]
  precio: float = Field(gt=0)

class RecambioCreate(RecambioBase):
  def to_orm_dict(self):
    d = super().dict(exclude_none=True)
    if 'dimensiones' in d:
      del d['dimensiones']
      d['alto'] = self.dimensiones.alto
      d['ancho'] = self.dimensiones.ancho
      d['largo'] = self.dimensiones.largo
    return d

class RecambioUpdate(BaseModel):
  nombre: Union[str, None] = None
  descripcion: Union[str, None] = None
  proveedor: Union[str, None] = None
  modelo: Union[str, None] = None
  cantidad: Union[int, None] = Field(None, ge=0)
  vehiculos_compatibles: Union[list[str], None] = None
  peso: Union[float, None] = Field(None, gt=0)
  dimensiones: Union[Dimensiones, None]
  precio: Union[float, None] = Field(gt=0)


# Schema de recambio equivalente
class RecambioEquivalenteId(TypedDict):
  recambioEquivalenteId: int
