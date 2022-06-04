from typing import Union

from fastapi.responses import JSONResponse


class JSONProblemResponse(JSONResponse):
  def __init__(self, type: str, title: str, detail: str, status_code: int,
               instance: str='about:blank', headers: Union[dict, None]=None) -> None:
    content = dict(type=type, title=title, status=status_code, detail=detail, instance=instance)
    super().__init__(content, status_code, headers, media_type='application/problem+json')

class JSONProblemResponse400(JSONProblemResponse):
  def __init__(self, detail: str) -> None:
    super().__init__(type='https://httpstatuses.com/400',
                     title='BAD REQUEST',
                     status_code=400,
                     detail=detail)

class JSONProblemResponse404(JSONProblemResponse):
  def __init__(self) -> None:
    super().__init__(type='https://httpstatuses.com/404',
                     title='NOT FOUND',
                     status_code=404,
                     detail='El recurso solicitado no está disponible.')

class JSONProblemResponse409(JSONProblemResponse):
  def __init__(self, detail: str) -> None:
    super().__init__(type='https://httpstatuses.com/409',
                     title='CONFLICT',
                     status_code=409,
                     detail=detail)

class JSONProblemResponse412(JSONProblemResponse):
  def __init__(self) -> None:
    super().__init__(type='https://httpstatuses.com/404',
                     title='PRECONDITION FAILED',
                     status_code=412,
                     detail='El ETag proporcionado no está actualizado.')
