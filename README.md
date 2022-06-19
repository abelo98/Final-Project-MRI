Ejecutar ademas:
- pip3 install fastapi
- pip install "uvicorn[standard]"

Como ejecutar el proyecto ?
- Situarse dentro de la carpeta engine
- Abrir una terminal en esa ubicacion
- Correr este comando en la terminal `uvicorn main:app`
- Abrir el navegador: http://127.0.0.1:8000/


Nota: Para probar el proyecto se debe copiar el todos los archivos y carpetas del corpus dentro de "./engine/corpus", pues el sistema a partir de ahi realiza el procesamiento. Para la version final se quiere que el usuario pueda introducir la ruta donde se encuentra el corpus dentro de su PC, y con ello ganar en usabilidad y facilitar la interaccion.
Para la entrega final tambien se ofrecera una entorno virtual(pipenv) listo para instalar las dependecias.
