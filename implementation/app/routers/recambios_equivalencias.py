from typing import Union
import os.path

from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from .. import schemas
from ..common.utils import get_ETag
from ..database import crud
from ..database.database import get_db
from ..common.exceptions import HTTP400Exception, HTTP404Exception, HTTP409Exception


router = APIRouter(prefix='/recambios/{recambioId}/equivalencias')



@router.get('')
def get_recambio_equivalencias(request: Request,
                               recambioId: int,
                               If_None_Match: Union[str, None]=Header(default=None), # ETag (Caché)
                               db: Session=Depends(get_db)):
  recambio = crud.read_recambio(db, recambioId)

  if recambio is None or not recambio.recambios_equivalentes:
    raise HTTP404Exception()


  lista_recambios_equivalentes = []
  base_url = str(request.base_url)[:-1]
  recambio_parent_url = base_url + '/recambios'
  for recambio_equivalente in recambio.recambios_equivalentes:
    recambio_equivalente_dict = recambio_equivalente.to_dict()
    links = {'parent': {'href': recambio_parent_url, 'rel': 'getListaRecambios postRecambio'},
             'self':   {'href': recambio_parent_url + f'/{recambio_equivalente_dict["id"]}', 'rel': 'getRecambio putRecambio deleteRecambio'}}
    recambio_equivalente_dict['links'] = links

    lista_recambios_equivalentes.append(recambio_equivalente_dict)

  links = {'parent': {'href': base_url + os.path.split(str(request.url.path))[0], 'rel': 'getRecambio putRecambio deleteRecambio'},
           'self':   {'href': base_url + str(request.url.path), 'rel': 'getListaEquivalencias postEquivalencia'}}

  content = {'recambios_equivalentes': lista_recambios_equivalentes, 'links': links}


  ETag = get_ETag(content)
  headers = {'ETag': ETag}

  if ETag == If_None_Match:
    return Response(headers=headers, status_code=304)

  return JSONResponse(content=content, headers=headers)



@router.post('')
def post_recambio_equivalencias(request: Request, recambioId: int, recambioEquivalenteId: schemas.RecambioEquivalenteId, db: Session=Depends(get_db)):
  recambioEquivalenteId = recambioEquivalenteId['recambioEquivalenteId']

  if recambioId == recambioEquivalenteId:
    info = ( "No puede añadirse un recambio como equivalente de sí mismo "
            f"(recambioId ({recambioId}) == recambioEquivalenteId ({recambioEquivalenteId}))")
    raise HTTP400Exception(info)

  recambio = crud.read_recambio(db, recambioId)

  if recambio is None:
    raise HTTP404Exception()

  recambio_equivalente = crud.read_recambio(db, recambioEquivalenteId)

  if recambio_equivalente is None:
    info = f"El recambio con id '{recambioEquivalenteId}' no existe."
    raise HTTP400Exception(info)

  if not recambio.aniadir_recambio_equivalente(recambio_equivalente):
    detail = f"Los recambios con ids '{recambioId}' y '{recambioEquivalenteId}' ya eran equivalentes."
    raise HTTP409Exception(detail)

  db.commit()


  base_url = str(request.base_url)[:-1]
  path = str(request.url.path)
  headers = {'Location': base_url + path + '/' + str(recambioEquivalenteId)}

  return Response(headers=headers, status_code=201)



@router.options('')
def options_recambio_equivalencias(recambioId: int):
  headers = {'Allow': 'GET,POST,OPTIONS'}
  return Response(headers=headers, status_code=204)



@router.get('/{recambioEquivalenteId}')
def get_recambio_equivalencias(request: Request, recambioId: int, recambioEquivalenteId: int, db: Session=Depends(get_db)):
  recambio = crud.read_recambio(db, recambioId)
  recambio_equivalente = crud.read_recambio(db, recambioEquivalenteId)

  recambios_exists = recambio is not None and recambio_equivalente is not None
  if not recambios_exists or recambio_equivalente not in recambio.recambios_equivalentes:
    raise HTTP404Exception()

  base_url = str(request.base_url)[:-1]
  recambio_parent_url = base_url + '/recambios'
  recambio_dict = recambio_equivalente.to_dict()
  links = {'parent': {'href': recambio_parent_url, 'rel': 'getListaRecambios postRecambio'},
           'self':   {'href': recambio_parent_url + f'/{recambio_dict["id"]}', 'rel': 'getRecambio putRecambio deleteRecambio'}}
  recambio_dict['links'] = links

  links = {'parent': {'href': base_url + os.path.split(str(request.url.path))[0], 'rel': 'getListaEquivalencias postEquivalencia'},
           'self':   {'href': base_url + str(request.url.path), 'rel': 'getEquivalencia deleteEquivalencia'}}
  recambio_equivalente_dict = {'recambio': recambio_dict, 'links': links}

  return JSONResponse(content=recambio_equivalente_dict)



@router.head('/{recambioEquivalenteId}')
def head_recambio_equivalencias(recambioId: int, recambioEquivalenteId: int, db: Session=Depends(get_db)):
  recambio = crud.read_recambio(db, recambioId)
  recambio_equivalente = crud.read_recambio(db, recambioEquivalenteId)

  recambios_exists = recambio is not None and recambio_equivalente is not None
  if not recambios_exists or recambio_equivalente not in recambio.recambios_equivalentes:
    raise HTTP404Exception()
  else:
    return Response(status_code=200)



@router.delete('/{recambioEquivalenteId}')
def delete_recambio_equivalencias(recambioId: int, recambioEquivalenteId: int, db: Session=Depends(get_db)):
  recambio = crud.read_recambio(db, recambioId)
  recambio_equivalente = crud.read_recambio(db, recambioEquivalenteId)

  recambios_exists = recambio is not None and recambio_equivalente is not None
  if not recambios_exists or recambio_equivalente not in recambio.recambios_equivalentes:
    raise HTTP404Exception()

  recambio.eliminar_recambio_equivalente(recambio_equivalente)
  db.commit()

  return Response(status_code=204)



@router.options('/{recambioEquivalenteId}')
def options_recambio_equivalencias(recambioId: int, recambioEquivalenteId: int):
  headers = {'Allow': 'GET,HEAD,DELETE,OPTIONS'}
  return Response(headers=headers, status_code=204)