

Esta seccion ignorala.

<!--Ejecutar además:-->

- <!--pip3 install fastapi-->
- <!--pip install "uvicorn[standard]"-->

<!--Como ejecutar el proyecto ?-->

- <!--Situarse dentro de la carpeta engine-->
- <!--Abrir una terminal en esa ubicacion-->
- <!--Correr este comando en la terminal `uvicorn main:app`-->
- <!--Abrir el navegador: http://127.0.0.1:8000/-->

<!--Nota: Para probar el proyecto se debe copiar el todos los archivos y carpetas del corpus dentro de "./engine/corpus", pues el sistema a partir de ahi realiza el procesamiento. Para la version final se quiere que el usuario pueda introducir la ruta donde se encuentra el corpus dentro de su PC, y con ello ganar en usabilidad y facilitar la interaccion. Para la entrega final tambien se ofrecera una entorno virtual(pipenv) listo para instalar las dependecias.-->



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

En el frontend se brinda la posibilidad de abrir cada documento, de forma tal que pueda revisarse el contenido de cada uno de los retornados y además la posibilidad de decir si es relevante o no; para ello se presenta la clase _Feedback_. 

_Feedback_ contiene dos métodos: `get_feedback` y `set_feedback`, luego lo que se pretende básicamaente es: por cada documento para para el que el usuario provea un feedback, almacenar de alguna forma que se manejó que para la consulta $X$ el documento $d_j$ era relevante.

Para garantizar el adecuado almacenamiento de estos datos y el acceso a los mismo de manera constante se emplea un _Trie_, que no es más que una estructura arborea para guardar cadena, y que la inserción y la búsqueda en los mismo son lineal respecto al tamaño de la cadena $O(|w|)$; luego la idea que se sigue es insertar la query (previamente procesada) en el trie y en el nodo final de esta se dejan dos _set()_ uno que marca los documentos relavantes para esa query y el otro marca los no relevantes; naturalmente, para cada documento se dejan sus índices en los sets. El uso del trie es  para evitar un poco el proceso de tener que hacer hash a partir de las queries, lo que quizá podría traer colisiones; en dependencia, claro está del número de queries que se realicen.

```python
class Feedback:
    def __init__(self):
        self.first: Node = Node()

    def set_feedback(self, _type: int, doc_id, query: List[str]):
        node = self.first

        for t in query:
            if not node.terms.__contains__(t):
                node.terms[t] = Node()

            node = node.terms[t]

        if _type == -1:
            if node.relevant_docs.__contains__(doc_id):
                node.relevant_docs.remove(doc_id)
            node.no_relevant_docs.add(doc_id)
        else:
            if node.no_relevant_docs.__contains__(doc_id):
                node.no_relevant_docs.remove(doc_id)
            node.relevant_docs.add(doc_id)

    def get_feedback(self, query: List[str]) -> Tuple[Set, Set]:
        node = self.first

        for t in query:
            if node.terms.__contains__(t):
                node = node.terms[t]
            else:
                return None

        return node.relevant_docs, node.no_relevant_docs
```



De qué forma influye el feedback brindando por los usuarios en los resultado de las próximas respuestas ?

Por cada nueva query que se realize, se efectua un reajuste en los pesos de términos de esta, lo que asegura que se de importancia al feedback que otros usuarios han brindado para la misma. En principio si para otra query con esos mismos términos ya se realizó algún feedback, lo que se hace es construir una nueva que responde a la siguiente estructura:
$$
\begin{align*}
q_n = q + \frac{\beta}{|R|} * d_r - \frac{\delta}{|NR|} &* d_{nr} \\
\beta = 0.5, \alpha = 1 \\
\end{align*}
$$
En otras palabras, los pesos de los términos de la nueva query serán la suma a los pesos originales del producto de una constante $\beta$ previamente definida y los pesos de esos términos en cada unos de los documentos relevantes, luego se sustrae el producto de la constante $\delta$, igualmente definida con anterioridad, y el peso de los términos en cada uno de los documentos para los que se brindó un feedback de no relevante.

El algoritmo en resumen lo que hace es darle mayor importancia a los términos más usados en los documentos considerados relevantes para los usuarios, y por el contrario, los términos más usados en los documentos no relevantes se les da menor importancia.



#### Aspectos generales del front:

El front se encuentra desarrollado en _Vue_, exponiendo una implementación en extremo sencilla, pero que es capaz que cubrir todas las necesidades del proyecto; se utilizó un servidor de vue durante el desarrollo del mismo, para posteriormente general los archivos estáticos necesarios para el correcto funcionamiento con la lógica escrita en python. Para realizar las peticiones al servidor de python se utliza _fetch_, interfaz que se encuentra expuesta y que es manejada por todos los navegadores actuales a la hora de consultar recursos.

De cualquier forma consultar el siguiente enlance para tener más detalles acerca de la implementación del mismo.

https://github.com/abelo98/Final-Project-MRI/tree/master/interface
