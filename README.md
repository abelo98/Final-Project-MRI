### Palabras clave:

**Sistemas de recuperación de información** (SRI), **procesamiento del lenguaje natural** (PLN), **motores de búsqueda** (MB), **Modelo de recuperación información** (MRI).

 ### Introducción

Como se ha ido comprobando a lo largo del curso, los sistemas de recuperación de información tienen que cumplir con el objetivo de otorgar documentos, responder preguntas, procesar paginas web y darles relevancia, entre otras muchas técnicas. Conocemos principalmente los motores de búsquedas dedicados a la tarea de recibir una consulta y entregar una serie de documentos y páginas web que considera relevantes. La explicación exacta de como funciona o qué fases realizan MBs como Chrome o mozilla va más allá del contenido que abarca este trabajo. Este trabajo está enfocado en el desarrollo de un modelo vectorial y otro booleano, que actúan sobre tres corpus distintos(Cran, Med y 20newsgroup).

El modelo vectorial se destaca por el empleo de vectores no binarios y por recuperar los documentos de acuerdo a su ranking de relevancia; esto le da un mayor índice de recuperación de documentos relevantes que el modelo booleano. Cuando hablamos de vectores no binarios, nos referimos a que los documentos pasan por un proceso donde se convierten a un vector, donde cada una de sus componentes son calculadas empleando la fórmula de $tf$ x $idf$, basada en la frecuencia de términos. Las queries pasan por un proceso similar para otorgar pesos a sus componentes y finalmente se determinan los  documentos más relevantes a una query mediante el cálculo del coseno de ángulo entre query y documento.

El modelo booleano se basa en la coincidencia exacta de términos entre el vector de la query con los documentos. Para ello emplea vectores booleanos y no hay existencia de un ranking por lo que todos los documentos son igual de relevantes. A pesar de ser más sencillo puede lograr buenos resultados con corpus que distingan bien sus temas y documentos.

Debemos destacar que solo existen tres modelos clásicos y sobre ellos se han ido construyendo otros más avanzados. Estos modelos "evolucionados" tienen diversas particularidades, como el uso de redes neuronales en el modelo vectorial o redes de inferencia en el probabilístico; esto los hace más certeros en cuanto a recuperar información. Incluso con el uso de estas evoluciones de los MRI, no debemos ser absolutos, pues no hay un modelo superior a otro, todo depende de sobre que corpus estemos trabajando, quiénes serán nuestros usuarios, para qué se desarrolla la el modelo, se quiere lograr eficiencia a coste de exactitud total de términos o mayor complejidad temporal en favor de obtener documentos relevantes sin total exactitud en los términos. Muchas son las preguntas que nos hacen decantarnos por un modelo y no por otro, y solo con el análisis de los posibles escenarios es posible una buena elección del Modelo de Recuperación de Información.



**Nota**

Debido al tamaño de las tablas de $idf$, $weight\_docs$ y $norm\_docs$, el peso de la aplicación llega a cerca de los $60$ mb. De lo contrario se debe esperar cerca de $40$ minutos a que se calculen estas tablas y luego realizar las consultas sin demora porque los binarios se guardan en su repo local.



#### Modelo Vectorial

El modelo vectorial es de los más empleados hoy en día en el campo de los SRI. Sus diferentes variantes hacen de este un modelo versátil capaz de desenvolverse bien en muchos escenarios. Para la correcta elaboración de este modelo dividimos su implementación en cuatro fases principales descritas a continuación:

**Procesamiento de documentos :**

En esta fase nos encargamos de dado un documento reducir su tamaño los más posible, de forma tal que su representación vectorial sea menor, se mantenga su idea central y términos claves. Para esta tarea empleamos la biblioteca de python $NLTK$, destinada al procesamiento del lenguaje natural que nos facilita el proceso de tokenizar el documento. Este trabajo se realiza en el módulo $text\_processor$ mediante la clase $Cleaner$. A continuación se muestra el código encargado de esta tarea:

```python
def doc_to_tokens(self, plain_text, use_stemmer=False, use_lematizer=False):
        # remove from:, mail addr and subject or Subject
        plain_text = self.__remove_especial_exp(plain_text)
		
        # tokenize and set to lower
        tokens = word_tokenize(plain_text)
        tokens = [t.lower() for t in tokens]
        
        # remove regular expr. 
        tokens = self.__remove_punct_reg(tokens)
        
        # filters all non words
        tokens = [word for word in tokens if word.isalpha()]
        
        # filters all stepwords
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if not t in stop_words]
        
        # word to root word
        if use_stemmer:
            stemmer = SnowballStemmer(language="english")
            tokens = [stemmer.stem(word) for word in tokens]

        if use_lematizer:
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(word) for word in tokens]
        return tokens

```

El flujo de trabajo con esta función es el siguiente

1. Eliminar las expresiones "From:", direcciones de correo y "Subject" o "subject".

2. Convertir las palabras en tokens y todas en minúscula.

3. Eliminar los signos de puntuación.
4. Eliminar todo lo que no represente palabras (Ej: números).

5. Eliminar las stopwords del inglés (Ej: and, for...).

6. Llevar las palabras a su raíz mediante el uso de lematizer o stemmer.

En las fases $1$ y $3$ Es necesario el uso de expresiones regulares capaz de reconocer y eliminar las cadenas no deseadas y los signos de puntuación. 

En la fase $6$ se toma una palabra y se lleva a su raíz. Se incluyen dos formas de realizar este proceso; la primera es mediante un algoritmo stemm, que no tiene en cuenta el significado de al palabra y elimina aquellos afijos que producen las variaciones morfológicas de la raiz. La segunda forma es mediante $WordNetLemmatizer$. Este algoritmo emplea la ontología $wordnet$ que permite reducir una palabra a su raíz manteniendo su sentido. Por ejemplo para el primer caso si tenemos languages, es reducida por el stemmer a languag y por el lematizer a language. En el primer caso se obtiene una palabra sin sentido y en el segundo si lo tiene. Estas dos formas de reducir palabras tiene sus pros y contras; por ejemplo si tuviéramos las siguientes palabras programmers, program y programming un stemmer reduce a program las palabras program y programming y un lematizer solo con program, manteniendo la otra igual. Sin embargo, para la palabra programmers un stemmer la reduce a programm que tiene sentido en alemán y no en inglés, aunque sea muy parecidas, y el lematizer la mantiene igual. Por tanto un stemmer puede lograr reducir más las dimensiones de un texto a cambio de perder sentido y un lematizer reduce menos manteniendo el sentido. En nuestro caso es más conveniente el empleo de un lematizer para poder expandir queries con sentido.

**Vectorización de documentos y cálculo de $tf$, $idf$ y pesos de componentes del documento:**

El módulo $core.py$ constituye el núcleo del motor de búsqueda. Este es el encargado de realizar todo el pipeline que permite la recuperación de documentos, pues mediante el se interactúa para realizar un request y obtener un response. Para llevar a cabo esta acción son necesarias varias fases como por ejemplo escanear el corpus de donde se van a extraer los documentos, levantar el modelo a emplear, inicializar el procesador de textos, cargar las tablas $tf$, $idf$, y vectores de documentos o calcularlas de no tenerlas. Todas estas fases son realizadas en este módulo, por lo que representa el centro neurológico del motor de búsqueda.

Una proceso de suma importancia es el que se lleva a cabo en la siguiente función:

```python
def start_search_engine_indexing(self):
        try:
            self.doc_tf = self.retrieve_from_disk(TF_DOCS_FILE)
            self.idf = self.retrieve_from_disk(IDF_FILE)
            self.doc_wights = self.retrieve_from_disk(DOCS_W)
            self.doc_norm = self.retrieve_from_disk(NORM_DOCS)
            self.query_exp.term_correlation = self.retrieve_from_disk(CORR)
        except:
            for dj, file in self.docs_id.items():
                plain_text = self.cl.get_text(file)
                tokens = self.cl.doc_to_tokens(plain_text, use_lematizer=True)
                self.query_exp.get_corr_in_text(tokens)
                self.__calc_tf(tokens, dj)

            self.__calc_idf()
            self.__calc_weights()

            self.save_to_disk(CORR, self.query_exp.term_correlation)
            self.save_to_disk(TF_DOCS_FILE, self.doc_tf)
            self.save_to_disk(IDF_FILE, self.idf)
            self.save_to_disk(DOCS_W, self.doc_wights)
            self.save_to_disk(NORM_DOCS, self.doc_norm)
     
```

  El flujo es el siguiente:

1. Intentar extraer del disco duro las tablas donde se almacenaron los $tf$, $idf$, vectores de documentos, normas de los vectores de documentos y la tabla de correlación de términos. 
2. Si existe algún problema en la fase anterior se procede a recorrer todos los ids y directorios de los documentos.
3. Se busca el docuemento original y luego se tokeniza y procesa el texto mediante la fase anteriormente explicada.
4. Se obtiene la matriz de correlación de términos.
5. Se calcula la tabla $tf$ de cada documento con sus términos.
6. Se calculan la tabla $idf$.
7. Cálculo de componentes del vector ($calc\_weights()$, función que se emplea también para calcular las normas de los vectores de los documentos).
8. Finalmente se guardan en el disco duro las tablas obtenidas.



En los puntos $1$ y $8$ se hace uso de la biblioteca $pickle$, mediante las funciones $retrieve\_from\_disk$ y $save\_to\_disk$ extrae y almacena respectivamente una estructura en el disco duro de forma encriptada.

##### Cálculo de tabla tf:

Para el punto $5$ se realiza la siguiente función:

```python
def __calc_tf(self, tokens, dj):
        aux = {}
        for t in tokens:
            try:
                aux[t, dj] += 1
            except KeyError:
                aux[t, dj] = 1
                try:
                    self.invert_index[t] += 1
                except KeyError:
                    self.invert_index[t] = 1

        max_freq_tok = max(aux.values())
        aux = {(key, dj): aux[key, dj] / max_freq_tok for key, _ in aux}
        self.doc_tf.update(aux)

```



En el código se emplean diccionarios para representar tablas. Este método recibe una lista de tokens del documento y el id del mismo. Luego, empleando un diccionario auxiliar que representa la frecuencia de tokens en el documento que se analiza, se revisa cada token, si ya se encuentra la llave $(token,id \space documento)$ significa que ese token ya ha sido visto en el documento y por tanto se aumenta la frecuencia en $1$, en el caso contrario se añade la llave con valor $1$ por ser la primera vez que se aparece en el documento.

La tabla $tf$ en $i,j$ indica la frecuencia con la que ocurre el término $i$ en el documento $j$, luego de ser normalizada. Para la normalización se divide la frecuencia del término $i$ entre la frecuencia del término que más se repite. 

Para mantener en cuantos documentos se encuentra el token $t$ se lleva otro diccionario $invert\_index$. $invert\_index{[}t{]}$ indica en la cantidad de documentos en que se encuentra el token $t$. Esto se empleará luego en el cálculo de la tabla $idf$.

Una vez revisada la lista de tokens del documento, se pasa a encontrar la frecuencia del token que más aparece, se divide cada valor del diccionario auxiliar por dicha frecuencia (normalización) y se actualiza el diccionario $tf$.

##### Cálculo de idf:

En el punto 6 se desarrolla mediante la siguiente función:

```python
def __calc_idf(self):
        for t in self.invert_index:
            self.idf[t] = math.log10(self.corpus_size / self.invert_index[t])
```

Para llevar a cabo el cálculo de la tabla $idf$ se emplea una función donde para cada término del cuerpo de documentos se aplica la fórmula de $idf_t = \log_{10}(\frac{N}{n_i})$. $N$ representa la cantidad de documentos del corpus, obtenida mediante el escaneo y $n_i$ es la cantidad de veces que se repite un término en todos los documentos. Esta fórmula es importante pues permite que un término que se repite demasiado no tenga más relevancia que uno que lo hace con menos frecuencia.

##### Cálculo del vector documento (tf * idf) y la norma:

El punto $7$ se efectúa mediante la siguiente función:

```python
def __calc_weights(self):
        for t in self.invert_index:
            for d in self.docs_id:
                try:
                    self.doc_wights[t, d] = self.doc_tf[t, d] * self.idf[t]
                except KeyError:
                    pass
        #calculate norms
        for dj in self.docs_id:
            self.doc_norm[dj] = np.linalg.norm([self.doc_wights[k] for k in self.doc_wights if k[1] == dj])
```

Finalmente para el cálculo de los pesos del vector documento la idea es ir por cada uno de los documentos y realizar la multiplicación $tf{[}t,d{]} * idf{[}t{]}$. Si se captura una excepción significa que el documento no posee el término y no es necesario mantener un cero o un valor extra en esa posición de la tabla. La última parte de este código refleja el método utilizado para calcular y mantener la norma del documento.

### Aspectos importantes

Aquí están plasmados algunos procesos análogos para cualquier corpus o modelo que se emplee.

**Empleo de métricas**

Para poder llevar a cabo una análisis de los modelos desarrollados se programaron las principales métricas estudiadas en conferencia: precisión, recobrado y $f_1$. Sabemos que para emplear estas métricas son necesarios la cardinalidad de los conjuntos de documentos relevantes recuperados ($rr$), relevantes no recuperados ($rn$) y los no relevantes recuperados $(nr)$, esto debido a:

- $P = \frac{rr}{rr+nr}$
- $R = \frac{rr}{rr+rn}$
- $f_1 = \frac{2PR}{P+R}$

Como la precisión y el recobrado se descompensan entre sí (si aumenta el recobrado disminuye la precisión y viceversa), es más fiable el análisis mediante $f_1$ que logra un equilibrio entre ambas métricas.

Las funciones empleadas para las métricas son las siguientes:

```python
def recoverd_docs(self, retrived_docs: dict, relevant_docs: list):
        rr = 0
        nr = 0
        for dicc in retrived_docs:
            if dicc['id'] in relevant_docs:
                rr += 1
            else:
                nr += 1
        return rr, nr

    def precision(self, retrived_docs: dict, relevant_docs: list):
        rr, nr = self.recoverd_docs(retrived_docs, relevant_docs)
        if rr and nr:
            return (rr / (rr + nr)) * 100
        else:
            return 0

    def recall(self, retrived_docs: dict, relevant_docs: list):
        rr, _ = self.recoverd_docs(retrived_docs, relevant_docs)
        rn = abs(len(relevant_docs) - rr)
        if rr and rn:
            return (rr / (rr + rn)) * 100
        else:
            return 0

    def f1(self, retrived_docs: dict, relevant_docs: list):
        p = self.precision(retrived_docs, relevant_docs)
        r = self.recall(retrived_docs, relevant_docs)
        if p != 0 or r != 0:
            return (2 * p * r / (p + r))
        else:
            return 0
```



La primera función es la encargada de devolvernos los documentos relevantes recuperados y los no relevantes recuperados, lo que se obtiene de forma sencilla si tenemos el conjunto de recuperados y de los considerados relevantes por los expertos.

**Nota**

Como apunte que debemos tener en cuenta los documentos que se consideran relevantes es debido a que un grupo de expertos determina su relevancia. Consideran un documento relevante si responde a queries definidas para  los corpus cran y med, para ello no necesariamente tienen que aparecer los términos de la query en el documento, pues puede ser que se responda con sinónimos o de otra forma.



**Parseo de corpus**

Los corpus cran y med tienen una forma particular en que están confeccionados. En el caso de cran, un documento tiene la siguiente estructura:

```
.I 1148
.T
knudsen flow through a circular capillary .
.A
w. c. demarcus and e. h. hopper
.B
carbide and carbon chemicals company, k-25 plant, post office box p,
oak ridge, tennessee
.W
knudsen flow through a circular capillary .
the problem of knudsen flow through a circular capillary has been
often discussed, usually by the momentum transfer method .  however,
p. clausing gave a rigorous formulation for the problem and obtained an
integral equation for which he gave an approximate solution .  from
time to time the accuracy of clausing's solution has been questioned
and since clausing did not give a rigorous estimate of his error we
have reinvestigated the problem .
```

Para el caso de med un ejemplo es el siguiente:

```
.I 1
.W
correlation between maternal and fetal plasma levels of glucose and free
fatty acids .                                                           
  correlation coefficients have been determined between the levels of   
glucose and ffa in maternal and fetal plasma collected at delivery .    
significant correlations were obtained between the maternal and fetal   
glucose levels and the maternal and fetal ffa levels . from the size of 
the correlation coefficients and the slopes of regression lines it      
appears that the fetal plasma glucose level at delivery is very strongly
dependent upon the maternal level whereas the fetal ffa level at        
delivery is only slightly dependent upon the maternal level .           
```

El módulo $parse\_corpus.py$ es el encargado de extraer cada documento de los corpus anteriores y crear un archivo para cada uno. Esto con el objetivo de que se puedan escanear de forma correcta. Para este objetivo es necesario pasar como primer argumento del módulo la dirección donde salvar cada documento extraído, dirección del corpus a procesar y nombre del corpus. Esto se hace con el objetivo de aplicar diferentes técnicas de extracción según el nombre del corpus, ya que los mismos no tiene una misma estructura.

**Testeo de los modelos:**

Para llevar a cabo el testeo de los diferentes modelos en cada corpus se creó el módulo $main.py$. Este módulo consta de las funciones necesarias para probar los corpus cran y med de forma automática y 20newsgroup de forma manual y analizar los resultados y métricas sin empleo de la API. Para automatizar el testeo de los corpus cran y med existen dos documentos que poseen un conjunto de queries para cada corpus y otros dos indincando para la query con número $x$ es relevante el documento $i$ con nivel de relevancia $j$.

**Escaneo del corpus:**

Este es el mecanismo mediante el cual se obtiene todos los posibles documentos a partir de una dirección. Para ello recursivamente analiza los subdirectorios y va conformando una lista con todos las direcciones de los documentos que encuentra. 

```python
def __scan_corpus(self, path) -> List[str]:
        if self.corpus_name == '20newsgroup':
            directories = listdir(path)
        else:
            directories = sorted(listdir(path), key=lambda e: int(e))
            
        files_found = []
        for e in directories:
            file_path = join(path, e)
            if not isfile(file_path):
                files_found += self.__scan_corpus(file_path)
            else:
                files_found.append(file_path)
        return files_found
```

Como se puede observar al inicio existe un pequeño conflicto sobre como listar el directorio. Esto se debe a que para probar y utilizar el corpus **cran** y **med** es necesario que los documentos estén listados en orden. Esto se debe a que su nombre es un número y es eso lo que se emplea para determinar el id del documento y poder determinar, entre otras cosas, que fueron relevantes para una query.

**Extracción de asuntos de documentos:**

funcionalidad implementada de esta clase es $get\_subjects$. Esta función es encargada de obtener los asuntos de los documentos que fueron recuperados y poder mostrarlos en el front para tener una perspectiva del documento. 

```python
def get_subjects(self, file_paths):
        subj = []
        for _, fp in file_paths:
            file = self.get_text(fp)
            subject = re.findall('Subject:[^\n]*', file)
            if subject:
                subject = subject[0].replace('Subject:', '')
                subject = subject.replace('Re:', '')
                subject = subject.strip()
            else:
                subject = fp

            subj.append(subject)
        return subj
```



#### Modelo booleano:

El modelo booleano es uno de los modelos clásicos de recuperación de información. Este está basado en la lógica booleana y la teoría de conjuntos. Los documentos a buscar y la consulta del usuario, son concebidos como un conjunto de términos. La representación está basada en cuando los documentos contienen o no a los términos de la consulta.

El modelo booleano posee, notablemente, ciertas ventajas que hace que quizá llame un poco la atención de quienes quieren adentrarse en el tema de la recuperación de información, puesto que es un modelo simple basado en conjuntos que presenta grandes facilidades a la hora de implementarlo y comprenderlo; pero por le otro lado posee también varias limitaciones radicando estas principalmente en el hecho de que no posee ranking, solo recupera los documentos donde la coincidencia es exacta - no hay correspondencia parcial -, además de considerar a todos los términos igual de importantes; por solo mencionar algunas. 

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
