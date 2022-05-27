# AOS-Implementacion-Servicio-Recambios

## Instrucciones para desplegar el servicio

El servicio está alojado en el registro de GitHub Packages de este mismo repositorio. Se puede obtener mediante el comando:
```console
$ docker pull ghcr.io/adrianja5/aos-implementacion-servicio-recambios:latest
```

Luego, el servicio se puede desplegar con el comando:
```console
$  docker run -p 80:8080 ghcr.io/adrianja5/aos-implementacion-servicio-recambios:latest
```
El contenedor utiliza el puerto `8080`, pero en el *host* se puede usar otro distinto (en el ejemplo se ha usado el puerto `80`).

Alternativamente, se puede utilizar otros *tags*:

### Tags disponibles

En construcción 🚧

## Construcción manual de las imágenes

### Servicio mock

Se puede obtener la imagen del servicio mock construyéndola manualmente siguiendo los pasos:

1. Clonar el repositorio de GitHub:
   ```console
   $ git clone https://github.com/adrianja5/AOS-Implementacion-Servicio-Recambios
   ```
2. Cambiar al directorio dónde se encuentra el fichero `Dockerfile` del servicio mock:
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

### Servicio implementado

En construcción 🚧

## Información del servicio implementado

En construcción 🚧
