from enum import Enum

class OrderParam(str, Enum):
  id = 'id'
  nombre = 'nombre'
  proveedor = 'proveedor'
  cantidad = 'cantidad'
  precio = 'precio'

class OrderingParam(str, Enum):
  ASC = 'ASC'
  DESC = 'DESC'