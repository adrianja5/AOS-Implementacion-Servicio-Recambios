from typing import List
from sqlalchemy import Table, CheckConstraint, Column, ForeignKey, Integer, PrimaryKeyConstraint, String, Float, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base



recambio_equivalente = Table('equivalencias_recambios', Base.metadata,
                             Column('id_recambio_1', Integer, ForeignKey('recambios.id'), nullable=False, index=True),
                             Column('id_recambio_2', Integer, ForeignKey('recambios.id'), nullable=False, index=True),
                             PrimaryKeyConstraint('id_recambio_1', 'id_recambio_2'))

vehiculo_compatible = Table('vehiculos_compatibles', Base.metadata,
                            Column('id_recambio', Integer, ForeignKey('recambios.id'), nullable=False, index=True),
                            Column('id_vehiculo', Integer, ForeignKey('vehiculos.id_vehiculo'), nullable=False, index=True),
                            PrimaryKeyConstraint('id_recambio', 'id_vehiculo'))

class Recambio(Base):
  __tablename__ = 'recambios'

  id = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(50), nullable=False)
  descripcion = Column(String(500))
  proveedor = Column(String(50), nullable=False)
  modelo = Column(String(50), nullable=False)
  cantidad = Column(Integer, nullable=False)
  peso = Column(Float)
  alto = Column(Float)
  ancho = Column(Float)
  largo = Column(Float)
  precio = Column(Float(precision=2), nullable=False)

  recambios_equivalentes: List["Recambio"] = relationship('Recambio',
                                                          secondary=recambio_equivalente,
                                                          primaryjoin=id==recambio_equivalente.c.id_recambio_1,
                                                          secondaryjoin=id==recambio_equivalente.c.id_recambio_2
                                                          )

  vehiculos_compatibles: List["Vehiculo"] = relationship('Vehiculo',
                                                         secondary=vehiculo_compatible,
                                                         back_populates='recambios_compatibles')

  __table_args__ = (UniqueConstraint('nombre', 'proveedor', 'modelo'),
                    CheckConstraint(cantidad >= 0, name='cantidad_mayor_igual_cero'),
                    CheckConstraint(peso > 0, name='peso_mayor_cero'),
                    CheckConstraint(precio > 0, name='precio_mayor_cero'))


  def to_dict(self):
    d = {col.name: getattr(self, col.name) for col in self.__table__.columns}

    if d['alto'] is not None or d['ancho'] is not None or d['ancho'] is not None:
      dimensiones = {}
      for dim in ['alto', 'ancho', 'largo']:
        dimensiones[dim] = d[dim]
    else:
      dimensiones = None
    for dim in ['alto', 'ancho', 'largo']:
      del d[dim]
    d['dimensiones'] = dimensiones

    vehiculos_compatibles = [vehiculo_compatible.nombre for vehiculo_compatible in self.vehiculos_compatibles]
    d['vehiculos_compatibles'] = vehiculos_compatibles

    return d

  def aniadir_recambio_equivalente(self, recambio: "Recambio"):
    if recambio not in self.recambios_equivalentes:
      self.recambios_equivalentes.append(recambio)
      recambio.recambios_equivalentes.append(self)
      return True
    else:
      return False

  def eliminar_recambio_equivalente(self, recambio: "Recambio"):
    if recambio in self.recambios_equivalentes:
      self.recambios_equivalentes.remove(recambio)
      recambio.recambios_equivalentes.remove(self)
      return True
    else:
      return False

class Vehiculo(Base):
  __tablename__ = 'vehiculos'

  id_vehiculo = Column(Integer, primary_key=True, index=True)
  nombre = Column(String(50), nullable=False, unique=True)

  recambios_compatibles = relationship('Recambio',
                                       secondary=vehiculo_compatible,
                                       back_populates='vehiculos_compatibles')
