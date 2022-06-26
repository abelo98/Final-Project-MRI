Ejecutar ademas:

- pip3 install fastapi
- pip install "uvicorn[standard]"

Como ejecutar el proyecto ?

- Situarse dentro de la carpeta engine
- Abrir una terminal en esa ubicacion
- Correr este comando en la terminal `uvicorn main:app`
- Abrir el navegador: http://127.0.0.1:8000/

Nota: Para probar el proyecto se debe copiar el todos los archivos y carpetas del corpus dentro de "./engine/corpus", pues el sistema a partir de ahi realiza el procesamiento. Para la version final se quiere que el usuario pueda introducir la ruta donde se encuentra el corpus dentro de su PC, y con ello ganar en usabilidad y facilitar la interaccion. Para la entrega final tambien se ofrecera una entorno virtual(pipenv) listo para instalar las dependecias.



#### Modelo booleano:

El modelo booleano es uno de los modelos clásicos de recuperación de información. Este está basado en la lógica booleana y la teoría de conjuntos, los documentos a buscar y la consulta del usuario, son concebidos como un conjunto de términos. La representación está basada en cuando los documentos contienen o no a los términos de la consulta.

El modelo booleano posee, notablemente, ciertas ventajas que hace que quizá llame un poco la antención de quienes quieren adentrarse en el tema de la recuperación de información, puesto que es un modelo simple basado en conjuntos que presenta grandes facilidades a la hora de implementarlo y comprenderlo; pero por le otro lado posee también varias limitaciones radicando estas principalmente en el hecho de que no posee ranking, solo recupera los documentos donde la coincidencia es exacta - no hay correspondencia parcial -, además de considerar a todos los términos igual de importantes; por solo mencionar algunas. 

La implementación del modelo se realizó auxiliándose de la tabla de _tf_ previamente computada. Esta contiene la frecuencia de cada término en los documentos y por tanto la información de si el término $t_j$ aparece en el documento $d_i$, que es precisamente lo que nos interesa saber en este caso. 

A la query por su parte se le aplica el proceso _tokenizacion_ donde se expanden las convierten las palabras a minúscula, se remueven los signos de puntuación, se remueven las palabras que contengan dígitos, asi como los stopwards y se aplica finalmente el proceso de lemantización; del mismo modo ocurre con el modelo vectorial.

Luego con la ayuda de los _set()_ de _python_ se va se va realizando el filtrado correspondiente para garantizar que los documentos que salgan al final de todo el proceso, sean precisamente los documentos que contienten todos los términos de las queries.

```python
ans = []
for t in query_tokens:
    temp = [id_doc for (ter, id_doc) in keys if ter == t]

    if len(ans) == 0:
        ans = temp.copy()

    ans = list(set(temp) & set(ans))

    if ans is None or len(ans) == 0:
        break

return [(id_doc, self.docs_ids[id_doc]) for id_doc in ans]

```



#### Proceso de retroalimentación:

En el frontend se brinda la posibilidad de abrir cada documento, de forma tal que pueda revisarse el contenido de cada uno de los retornados y además la posibilidad de decir si es relevante o no. Por lo que tenemos la clase **Feedback**

La cual contiene dos métodos: `get_feedback` y `set_feedback`, entonces por cada documento que nos den feedback haciendo uso de un trie(trie es una estructura de datos para guardar cadenas, con costo lineal en tiempo con respecto al tamaño de la cadena) podemos insertar una query y en el nodo final tendremos un set con los ínidices de los documentos relevantes y otro set con los ínidices de los no relevantes, si en algún momento decimos que el documento *d* era no relevante y ahora el usuario lo clasificó como relevante en esa query entonces lo eliminamos del set de no relevantes y lo añadimos en el de relevantes, y viceversa. El uso del trie es con el objetivo de evitar hacer hash a las query, hashes que luego puedan traer coliciones y ya que podemos tener muchísimas queries en feedback, este caso es posible.
