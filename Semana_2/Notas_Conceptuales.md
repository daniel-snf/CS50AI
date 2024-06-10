# Notas
> Daniel Camacho

# Redes Bayesianas
Pueden ser vistas como estructuras de datos que representan dependencias entre variables aleatorias, estas contienen:

- Grafo Dirigido
- Cada nodo representa una variable aleatoria
- Cada flecha de $X$ a $Y$ significa que $X$ es padre de $Y$, dependencia.
- Cada nodo de $X$ tiene una distribución de probabilidad $P(X|Pariente(X))$

## Inferencia
Se tiene
- Query $X$: Variable por la cual se computa una distribución
- Variables de evidencia: $E$ variable observadas para el evento $e$
- Variables ocultas $Y$: Variables no-evidencia, y non-query 

- Objetivo: Calcular $P(X|e)$

Un método es la inferencia mediante enumeración, tiene la siguiente forma:

$$P(X|e) = \alpha P(X,e) = \alpha \sum_y P(X,e,y)$$

En donde:

- $X$ es la variable Query
- $e$ es la evidencia 
- $y$ rango de valores en el que hay variables ocultas
- $\alpha$ normaliza el resultado (Para que sume a uno)

Y existen muchas formas de optimizar este procedimiento, pero aún así para una red muy amplia este proceso puede ser un tanto ineficiente.

Para hacer **inferencia aproximada** un método es el conocido como 

## Muestreo/Sampling
En donde se toma una muestra de todas las variables dentro de la red bayesiana en estudio, lo cual se vuelve muy poderoso si se realiza muchas veces de manera repetida.

Y se genera una gran cantidad de muestras, y en base a la información de esta se realiza la inferencia de los Query, con este método de muestreo llamado muestreo de rechazo puede que solo se tomen unos casos y se rechazen otros haciendo que sea muy ineficaz todo el muestreo necesario. 

Así un metood de muestreo mas apropiado es **Likelihood Weighting**

El cual consiste en un procedimiento similar en donde se intenta evitar el descartar muestras que no encajen con la evidencia. 

La receta detras de el procedimiento es:

- Fijando los valores de la evidencia
- Muestrear valores de no-evidencia usando probabilidades condicionales en la red bayesiana
- Pesar cada muestra por su **Verosimilitud**: probabilidad de toda la evidencia

# Modelos Markovianos
Introducimos los modelos Markovianos para lidiar con incertidumbre con respecto al tiempo. 

### Supuestos
**Supuesto Markoviano**
La suposición de que el estado actual depende solamente de un número finito de estados previos. *perdida de memoria* o se puede ver como que el futuro es independiente del pasado dado el momento presente. 

### Cadena Markoviana
Secuencia de variables aleatorias donde la distribución de probabilidad de cada variable sigue el supuesto markoviano.

Y en el modelo markoviano como sabemos la matriz de transiciónes nos expresa los resultados probabilisticos del modelo

### Hidden Markov Models
Modelo markoviano con con estados ocultos que generan un evento observado.

Basado en la **suposición markoviana sensorial**, la cual asume que la *evidence variable* depende solamente del estado correspondiente. 