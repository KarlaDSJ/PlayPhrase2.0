# PlayPhrase2.0
Procesamiento del lenguaje natural
Se intentará replicar la página [*PlayPhrase*](https://www.playphrase.me/#/search) 

## Equipo de trabajo:
- David, [*davidalencia*](https://github.com/davidalencia)
- Karla, [*KarlaDSJ*](https://github.com/KarlaDSJ)

### Con ayuda de:
- Emilio, [*milmor*](https://github.com/milmor)
- Víctor, [*VMijangos*](https://github.com/VMijangos)
___

<a id="indice"></a>
## Tareas:

1. [**Corpus**](#corpus)

2. [**Recuperación de información**](#RI)

3. [**Agrupación**](#clusters)
___

<a id="corpus"></a>
### Corpus <small>[[Top](#indice)]</small>
Creamos un programa en donde que nos permite extraer los subtítulos de vídeos de Youtube junto con el tiempo en el que aparecen.

Los canales utilizados para esta tarea son:

|           id            |    canal      |
|-------------------------|---------------|
|UCshVTOdmZLdLj8LTV1j_0uw | tedespañol    |
|UCZcvCpFcLxOKGbMocVgLjEA | kurzgesagt    |
|UC3uPK6zOTe0HOfcIkuzII0Q | disneyplusla  |
|UCBSs9x2KzSLhyyA9IKyt4YA | netflixanime  |
|UCrVhY_d0L0qayRhMsRlPBOA | 31minutostv   |
|UCJQQVLyM6wtPleV4wFBK06g | visualpolitik |
|UC_Zc2fmbDpu_arkwvCDcX5g | cocina        |
|UCyQqzYXQBUWgBTn4pw_fFSQ | auronplay     |
|UCX6b17PVsYBQ0ip5gyeme   | crash course  |

Utilizamos estos canales porque hablan de temas muy variados.

El código que genera el corpus se encuentra en la carpeta corpus/ y la carpeta donde se encuentras los datos después de ejecutar el programa es corpus/data

#### Instalación 
```
cd corpus
npm install
```

#### Ejecución
```
cd corpus
node index.js
```

Además el análisis del corpus se hace en el notebook Estadisticas.ipynb

<a id="RI"></a>
### Recuperación de información <small>[[Top](#indice)]</small>
La tarea que se plantea es que dada una cadena (query) el programa nos muestre el subtítulo de algún video que se encuentra en el corpus que más se le parezca, así como la información para en un futuro se muestre el fragmento de ese vídeo, para completar esta tarea intentamos lo siguiente:

- TF-IDF (notebook TF-IDF.ipynb)
    - Por subtítulo
    - Por video

- Levenshtein con palabras (notebook FauxLeveshtein.ipynb)

- Doc2Vec (notebook Doc2Vec.ipynb)

Los resultados obtenidos son los siguientes (notebook Metricas.ipynb):

|   Método    | Precision | Recall | Accuracy |   F1   |
|-------------|-----------|--------|----------|--------|
|TF-IDF sub   |     1     | 0.3012 |  0.4407  | 0.4630 |
|TF-IDF video |     1     | 0.1458 |  0.3163  | 0.2545 |
|Levenshtein  |           |        |          |        |
|Doc2Vec      |     1     | 0.3991 |  0.5190  | 0.5705 |

<a id="clusters"></a>
### Agrupación <small>[[Top](#indice)]</small>

K-means (notebook Agrupar.ipynb)

- Utilizando vectores TF-IDF por documento
- Utilizando Doc2Vec por el título de cada video

Como un intento de analizar los clusters notebook EvalAgrupar.ipynb

