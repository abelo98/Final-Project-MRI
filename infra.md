#### Cómo ejecutar el proyecto ?

Para la ejecución de la aplicación se hace necesario manejar ciertas depedencias que dejaremos descritas en esta sección del informe.

En el proyecto se encuetra actualmente configurado un entorno virtual para la ejecución del mismo por medio de pipenv; por tanto se hace necesario contar con ese paquete instalado para poder ejecutar la instalación de todas las dependencias de forma automática y no tener que preocuparse por esa questión; de cualquier manera se puede realizar de las dos formas.

Cómo instalar pipenv ? 

> pip3 install pipenv

Cómo ejecutar el proyecto una vez instalado pipenv.

```bash
cd `project root`
pipenv shell
pipenv install --ignore-pipfile
```

Los comandos anteriores garantizan la instalación adecuada de todas las dependencias del proyecto.

De cualquier modo es probable que haya que descargar los útiles para el funcionamiento de nltk de forma manual, para ello seguir los siguientes pasos.

```bash
cd `project root`
python3
import nltk
nltk.download(´paquete´)
```



Cada _paquete_ debe cambiarse por el nombre real del paquete y es necesario contar con los siguientes instalados.

- stopwords
- averaged_perceptron_tagger
- wordnet
- omw-1.4
- punkt

Una vez que se encuentren correctamente instaladas todas las dependencias, ya sea por medio del entorno virtual o manualmente, ejecutamos el siguiente comando para correr la aplicación.

> uvicorn main:app

Esta operación crea un servidor que se ejecuta por el puerto 8000 de 127.0.0.1; por tanto para solo resta abrir el navegador e introducir la siguiente dirección:

http://127.0.0.1:8000
