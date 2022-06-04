import re

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware


from .routers import recambios, recambios_equivalencias
from .database import models, database
from .json_problem_responses import JSONProblemResponse400, JSONProblemResponse404, JSONProblemResponse409, JSONProblemResponse412
from .common.exceptions import HTTP400Exception, HTTP404Exception, HTTP409Exception, HTTP412Exception

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title='recambios', redoc_url=None)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["etag", "location"]
)



app.include_router(recambios.router, prefix='/api/v1')
app.include_router(recambios_equivalencias.router, prefix='/api/v1')

######################
# Exceptions handlers
######################

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
  info = re.sub(r'\([^)]*\)', '', str(exc)).rstrip()
  detail = 'Se ha introducido algún valor erróneo. Más información:\n' + info
  return JSONProblemResponse400(detail)

@app.exception_handler(HTTP404Exception)
def HTTP_404_handler(request: Request, exc: HTTP404Exception):
  return JSONProblemResponse404()

@app.exception_handler(HTTP400Exception)
def HTTP_400_handler(request: Request, exc: HTTP400Exception):
  return JSONProblemResponse400(exc.detail)

@app.exception_handler(HTTP409Exception)
def HTTP_409_handler(request: Request, exc: HTTP409Exception):
  return JSONProblemResponse409(exc.detail)

@app.exception_handler(HTTP412Exception)
def HTTP_409_handler(request: Request, exc: HTTP412Exception):
  return JSONProblemResponse412()
