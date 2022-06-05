from typing import Union
import urllib.parse
import os.path
from math import ceil

from fastapi import APIRouter, Depends, Header, Query, Request
from fastapi.responses import JSONResponse, Response
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import schemas
from ..common.utils import get_ETag
from ..database import crud, models
from ..database.database import get_db
from ..common.enums import OrderingParam, OrderParam
from ..common.exceptions import HTTP404Exception, HTTP409Exception, HTTP412Exception


router = APIRouter(prefix='/recambios')



@router.get('')
def get_recambios(request: Request,
                  page: int=Query(ge=1, default=1), limit: int=Query(ge=0, default=10), # Paginación
                  order: OrderParam=OrderParam.id, ordering: OrderingParam=OrderingParam.ASC, # Ordenar
                  nombreFilter: Union[str, None]=None, # Filtrar
                  If_None_Match: Union[str, None]=Header(default=None), # ETag (Caché)
                  db: Session=Depends(get_db)):

  if limit == 0 and page != 1: # Con limit == 0 hay solo una página
    raise HTTP404Exception()

  recambios = crud.read_recambios(db, page, limit, order, ordering, nombreFilter)

  if len(recambios) == 0:
    raise HTTP404Exception()


  lista_recambios = []
  base_url = str(request.base_url)[:-1]
  recambio_parent_url = base_url + str(request.url.path)
  for recambio in recambios:
    recambio_dict = recambio.to_dict()
    links = {'parent': {'href': recambio_parent_url, 'rel': 'getListaRecambios postRecambio'},
             'self':   {'href': recambio_parent_url + f'/{recambio_dict["id"]}', 'rel': 'getRecambio putRecambio deleteRecambio'}}
    recambio_dict['links'] = links

    lista_recambios.append(recambio_dict)


  common_params = {'limit': limit, 'order': order.value, 'ordering': ordering.value}
  if nombreFilter is None:
    total_recambios = db.query(func.count(models.Recambio.id)).scalar()
  else:
    total_recambios = db.query(func.count(models.Recambio.id)).filter(models.Recambio.nombre.contains(nombreFilter)).scalar()
    common_params['nombreFilter'] = nombreFilter


  first_params = {'page': 1} | common_params
  if limit == 0:
    last_page = 1
  else:
    last_page = ceil(total_recambios/limit)
  last_params = {'page': last_page} | common_params
  current_params = {'page': page} | common_params


  rel = 'getListaRecambios'
  links = {'first': {'href': recambio_parent_url + '?' + urllib.parse.urlencode(first_params), 'rel': rel},
           'last':  {'href': recambio_parent_url + '?' + urllib.parse.urlencode(last_params),  'rel': rel}}
  if page != 1: # Si no es la primera página
    prev_params = current_params.copy()
    prev_params['page'] = prev_params['page'] - 1
    links['prev'] = {'href': recambio_parent_url + '?' + urllib.parse.urlencode(prev_params), 'rel': rel}

  if page != last_page: # Si no es la última página
    next_params = current_params.copy()
    next_params['page'] = next_params['page'] + 1
    links['next'] = {'href': recambio_parent_url + '?' + urllib.parse.urlencode(next_params), 'rel': rel}


  content = {'recambios': lista_recambios, 'links': links}

  ETag = get_ETag(content)
  headers = {'ETag': ETag}

  if ETag == If_None_Match:
    return Response(headers=headers, status_code=304)

  return JSONResponse(content=content, headers=headers)



@router.post('')
def post_recambio(request: Request, recambio: schemas.RecambioCreate, db: Session=Depends(get_db)):
  recambio_unico = crud.read_recambio_unico(db, recambio.nombre, recambio.proveedor, recambio.modelo)

  if recambio_unico is not None:
    detail = f"El recambio con nombre: '{recambio.nombre}', proveedor: '{recambio.proveedor}' y modelo: '{recambio.modelo}' ya existe."
    raise HTTP409Exception(detail=detail)

  recambio_creado = crud.create_recambio(db, recambio_dict=recambio.to_orm_dict())

  base_url = str(request.base_url)[:-1]
  path = str(request.url.path)
  headers = {'Location': base_url + path + '/' + str(recambio_creado.id)}

  return JSONResponse(content=recambio_creado.to_dict(), headers=headers, status_code=201)



@router.options('')
def options_recambios():
  headers = {'Allow': 'GET,POST,OPTIONS'}
  return Response(headers=headers, status_code=204)



@router.get('/{recambioId}')
def get_recambio(request: Request, recambioId: int, db: Session=Depends(get_db)):
  recambio = crud.read_recambio(db, recambioId)

  if recambio is None:
    raise HTTP404Exception()

  recambio = recambio.to_dict()
  ETag = get_ETag(recambio)
  headers = {'ETag': ETag}


  base_url = str(request.base_url)[:-1]
  links = {'parent': {'href': base_url + os.path.split(str(request.url.path))[0], 'rel': 'getListaRecambios postRecambio'},
           'self':   {'href': base_url + str(request.url.path), 'rel': 'getRecambio putRecambio deleteRecambio'}}
  recambio['links'] = links

  return JSONResponse(content=recambio, headers=headers)



@router.put('/{recambioId}')
def put_recambio(request: Request, recambioId: int, recambio_updates: schemas.RecambioUpdate, If_Match: str=Header(default=None), db: Session=Depends(get_db)):
  old_recambio = crud.read_recambio(db, recambioId)

  if old_recambio is None:
    raise HTTP404Exception()

  ETag_old_recambio = get_ETag(old_recambio.to_dict())
  if If_Match != ETag_old_recambio:
    raise HTTP412Exception()

  recambio_updates_dict = recambio_updates.dict(exclude_none=True)
  if 'dimensiones' in recambio_updates_dict:
    recambio_updates_dict = recambio_updates_dict | recambio_updates_dict['dimensiones']
    del recambio_updates_dict['dimensiones']

  nombres_vehiculos_compatibles = recambio_updates_dict.pop('vehiculos_compatibles', None)

  if recambio_updates_dict:
    crud.update_recambio(db, recambioId, recambio_updates_dict)

  if nombres_vehiculos_compatibles is not None:
    crud.update_recambio_vehiculos_compatibles(db, recambioId, nombres_vehiculos_compatibles)

  recambio_updated = crud.read_recambio(db, recambioId)

  recambio_updated = recambio_updated.to_dict()
  base_url = str(request.base_url)[:-1]
  links = {'parent': {'href': base_url + os.path.split(str(request.url.path))[0], 'rel': 'getListaRecambios postRecambio'},
           'self':   {'href': base_url + str(request.url.path), 'rel': 'getRecambio putRecambio deleteRecambio'}}
  recambio_updated['links'] = links


  return JSONResponse(content=recambio_updated)



@router.delete('/{recambioId}')
def delete_recambio(recambioId: int, db: Session=Depends(get_db)):
  if crud.delete_recambio(db, recambioId):
    return Response(status_code=204)
  else:
    raise HTTP404Exception()



@router.options('/{recambioId}')
def options_recambio(recambioId: int):
  headers = {'Allow': 'GET,PUT,DELETE,OPTIONS'}
  return Response(headers=headers, status_code=204)
