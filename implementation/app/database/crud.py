from sqlalchemy.orm import Session

from . import models
from ..common.enums import OrderParam, OrderingParam


def read_recambio(db: Session, recambio_id: int):
  return db.query(models.Recambio).filter(models.Recambio.id == recambio_id).first()

def read_recambio_unico(db: Session, nombre: str, proveedor: str, modelo: str):
  recambio = db.query(models.Recambio).filter(models.Recambio.nombre == nombre,
                                              models.Recambio.proveedor == proveedor,
                                              models.Recambio.modelo == modelo).first()

  return recambio

def read_recambios(db: Session, page: int, limit: int, order: OrderParam, ordering: OrderingParam, nombreFilter: str=None):
  column_to_order = getattr(models.Recambio, order.value)
  if ordering is OrderingParam.ASC:
    column_to_order = column_to_order.asc()
  else:
    column_to_order = column_to_order.desc()

  query = db.query(models.Recambio)

  if nombreFilter is not None:
    query = query.filter(models.Recambio.nombre.contains(nombreFilter))

  query = query.order_by(column_to_order).offset((page - 1) * limit)

  if limit != 0:
    query = query.limit(limit)

  return query.all()

def create_recambio(db: Session, recambio_dict: dict):
  nombres_vehiculos_compatibles = recambio_dict.pop('vehiculos_compatibles', None)

  db_recambio = models.Recambio(**recambio_dict)

  if nombres_vehiculos_compatibles is not None:
    nombres_vehiculos_compatibles = set(nombres_vehiculos_compatibles)
    for nombre_vehiculo_compatible in nombres_vehiculos_compatibles:
      vehiculo_compatible = db.query(models.Vehiculo).filter(models.Vehiculo.nombre == nombre_vehiculo_compatible).first()
      if vehiculo_compatible is None:
        vehiculo_compatible = models.Vehiculo(nombre=nombre_vehiculo_compatible)
      db_recambio.vehiculos_compatibles.append(vehiculo_compatible)

  db.add(db_recambio)
  db.commit()
  db.refresh(db_recambio)

  return db_recambio

def update_recambio(db: Session, id_recambio: int, recambio_update: dict):
  db.query(models.Recambio).filter_by(id=id_recambio).update(recambio_update)
  db.commit()

def delete_recambio(db: Session, id_recambio: int) -> bool:
  db_recambio = db.query(models.Recambio).filter_by(id=id_recambio).one_or_none()
  if db_recambio is None:
    return False

  recambios_equivalentes = []
  recambios_equivalentes[:] = db_recambio.recambios_equivalentes

  for recambio_equivalente in recambios_equivalentes:
    db_recambio.eliminar_recambio_equivalente(recambio_equivalente)

  ## Borrar los vehículos que han quedado huerfanos (sin un recambio compatible)
  ids_vehiculos_compatibles_huerfanos = [vehiculo_compatible_eliminado.id_vehiculo for vehiculo_compatible_eliminado
                                                                                   in db_recambio.vehiculos_compatibles
                                                                                   if len(vehiculo_compatible_eliminado.recambios_compatibles) == 1] # Si es 1 solo está en el recambio a eliminar

  for id_vehiculo_compatible_huerfano in ids_vehiculos_compatibles_huerfanos:
    vehiculo = db.query(models.Vehiculo).filter_by(id_vehiculo=id_vehiculo_compatible_huerfano).one()
    db.delete(vehiculo)

  db.delete(db_recambio)
  db.commit()

  return True

def update_recambio_vehiculos_compatibles(db: Session, id_recambio: int, nombres_vehiculos_compatibles_new: list):
  db_recambio = db.query(models.Recambio).filter_by(id=id_recambio).first()

  if db_recambio is None:
    return False

  nombres_vehiculos_compatibles_old = [vehiculo_compatible.nombre for vehiculo_compatible in db_recambio.vehiculos_compatibles]


  # Añadir vehículos que no estaban
  nombres_vehiculos_compatibles_add = set(nombres_vehiculos_compatibles_new).difference(nombres_vehiculos_compatibles_old)
  for nombre_vehiculo_compatible in nombres_vehiculos_compatibles_add:
    vehiculo_compatible = db.query(models.Vehiculo).filter(models.Vehiculo.nombre == nombre_vehiculo_compatible).first()
    if vehiculo_compatible is None:
      vehiculo_compatible = models.Vehiculo(nombre=nombre_vehiculo_compatible)

    db_recambio.vehiculos_compatibles.append(vehiculo_compatible)

  # Borrar vehículos que no están
  nombres_vehiculos_compatibles_del = set(nombres_vehiculos_compatibles_old).difference(nombres_vehiculos_compatibles_new)
  db_recambio.vehiculos_compatibles = [vehiculo_compatible for vehiculo_compatible
                                                           in db_recambio.vehiculos_compatibles
                                                           if vehiculo_compatible.nombre not in nombres_vehiculos_compatibles_del]

  vehiculos_compatibles_eliminados = db.query(models.Vehiculo).filter(models.Vehiculo.nombre.in_(nombres_vehiculos_compatibles_del)).all()


  ## Borrar los vehículos que han quedado huerfanos (sin un recambio compatible)
  ids_vehiculos_compatibles_huerfanos = [vehiculo_compatible_eliminado.id_vehiculo for vehiculo_compatible_eliminado
                                                                                   in vehiculos_compatibles_eliminados
                                                                                   if not vehiculo_compatible_eliminado.recambios_compatibles]


  for id_vehiculo_compatible_huerfano in ids_vehiculos_compatibles_huerfanos:
    vehiculo = db.query(models.Vehiculo).filter_by(id_vehiculo=id_vehiculo_compatible_huerfano).one()
    db.delete(vehiculo)

  db.commit()
