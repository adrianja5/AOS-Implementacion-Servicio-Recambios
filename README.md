# AOS-Implementacion-Servicio-Recambios

## Instrucciones para desplegar el servicio

El servicio está alojado en el registro de GitHub Packages de este mismo repositorio. Se puede obtener mediante el comando:
```console
$ docker pull ghcr.io/adrianja5/aos-implementacion-servicio-recambios:latest
```

Luego, el servicio se puede desplegar con el comando:
```console
$ docker run -p 80:8080 ghcr.io/adrianja5/aos-implementacion-servicio-recambios:latest
```
El contenedor utiliza el puerto `8080`, pero en el *host* se puede usar otro distinto (en el ejemplo se ha usado el puerto `80`).

Alternativamente, se puede utilizar otros *tags*:

### Tags disponibles

Hay dos *tags* principales disponibles:

  - [`latest`](https://github.com/adrianja5/AOS-Implementacion-Servicio-Recambios/blob/main/implementation/Dockerfile): Hace referencia a la última versión de la API. Actualmente corresponde a la API implementada. Es la etiqueta que se **debe** usar para obtener la última versión de la API.
  - [`mock`](https://github.com/adrianja5/AOS-Implementacion-Servicio-Recambios/blob/main/mock/Dockerfile): Hace referencia a la última versión del *mock* de la API.

Además, hay un registro de las versiones de las imágenes de la implementación de la API que se puede consultar en la [información de la imagen](https://github.com/adrianja5/AOS-Implementacion-Servicio-Recambios/pkgs/container/aos-implementacion-servicio-recambios).

## Endpoints

Los endpoints disponibles y sus métodos son:

  - `/api/v1/recambios`: `GET`, `POST`, `OPTIONS`.
  - `/api/v1/recambios/{recambioId}`: `GET`, `PUT`, `DELETE`, `OPTIONS`.
  - `/api/v1/recambios/{recambioId}/equivalencias`: `GET`, `POST`, `OPTIONS`.
  - `/api/v1/recambios/{recambioId}/equivalencias/{recambioEquivalenteId}`: `GET`, `HEAD`, `DELETE`, `OPTIONS`.

Para más información, consultar la [especificación OpenAPI](https://github.com/adrianja5/AOS-Especificacion-Servicio-Grupo3).

## Construcción manual de las imágenes

### Servicio implementado

Se puede obtener la imagen del servicio implementado construyéndola manualmente siguiendo los pasos:

1. Clonar el repositorio de GitHub:
   ```console
   $ git clone https://github.com/adrianja5/AOS-Implementacion-Servicio-Recambios
   ```
2. Cambiar al directorio dónde se encuentra el fichero `Dockerfile` del servicio implementado:
   ```console
   $ cd AOS-Implementacion-Servicio-Recambios/implementation
   ```
3. Construir la imagen del servicio, indicando el nombre de la imagen en **minúsculas** y un *tag* opcional:
   ```console
   $ docker build --tag aos-implementacion-servicio-recambios:latest .
   ```
4. Desplegar el servicio usando el nombre de la imagen y el *tag* usado en el punto 3 e indicando los puertos, tanto del *host* 
   como del contenedor. El puerto interno del contenedor es el `8080`, pero el externo puede ser otro distinto (`80` en el ejemplo):
   ```console
   $ docker run -p 80:8080 aos-implementacion-servicio-recambios:latest
   ```

### Servicio mock

Se puede obtener la imagen del servicio *mock* construyéndola manualmente siguiendo los pasos, muy similares a los de la construcción de la imagen del servicio implementado:

1. Clonar el repositorio de GitHub:
   ```console
   $ git clone https://github.com/adrianja5/AOS-Implementacion-Servicio-Recambios
   ```
2. Cambiar al directorio dónde se encuentra el fichero `Dockerfile` del servicio *mock*:
   ```console
   $ cd AOS-Implementacion-Servicio-Recambios/mock
   ```
3. Construir la imagen del servicio, indicando el nombre de la imagen en **minúsculas** y un *tag* opcional:
   ```console
   $ docker build --tag aos-implementacion-servicio-recambios:mock .
   ```
4. Desplegar el servicio usando el nombre de la imagen y el *tag* usado en el punto 3 e indicando los puertos, tanto del *host* 
   como del contenedor. El puerto interno del contenedor es el `8080`, pero el externo puede ser otro distinto (`80` en el ejemplo):
   ```console
   $ docker run -p 80:8080 aos-implementacion-servicio-recambios:mock
   ```

## Ejemplo despliegue

En el directorio `example` se incluye un fichero `docker-compose.yaml` que sirve de ejemplo de despligue del servicio, incluyendo la gestión de la persistencia mediante volúmenes y la comunicación con otro servicio, una interfaz Swagger con la especificación del servicio.

**NOTA**: Es necesario clonar el repositorio ya que el servicio de interfaz Swagger hace uso de ficheros incluidos en este.
