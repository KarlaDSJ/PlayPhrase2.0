# PlayPhrase2.0
Procesamiento del lenguaje natural
Se intentará replicar la página [*PlayPhrase*](https://www.playphrase.me/#/search) 

## Equipo de trabajo:
- David, [*davidalencia*](https://github.com/davidalencia)
- Karla, [*KarlaDSJ*](https://github.com/KarlaDSJ)

## Corpus
Creamos un programa en node que nos permite extraer los subtítulos de vídeos de Youtube junto con el tiempo en el que aparecen.

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

Utilizamos estos canales porque hablan de temas muy variados

### Instalación 
```
cd corpus
npm install
```

### Ejecución
```
cd corpus
node index.js
```