import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    # El diccionario que representara la distribución de probabilidad de la
    # pagina que el random surfer visitara despues dado on corpus de paginas,
    # una pagina actual, y un damping factor (argumentos de la función)
    distribucion_probabilidades = {}

    
    ## El no_damping_factor = 1 - d
    no_damping_factor = 1 - damping_factor

    ## Número total de paginas en el corpus = N
    N = len(corpus)
    
    ## Número de links
    Num_Links = len(corpus[page])

    # Empezando con el caso de que no tenga enlaces 
    ## En ese caso "transition_model" devuelve la distribución de probabilidad que
    ## escoje aleatoreamente todas las paginas con equiprobabilidad. 
    ## (si no tiene links, se asume que tiene links a todas incluyendose ella misma)

    if Num_Links == 0:
        for i in corpus.keys():
            distribucion_probabilidades[i] = 1 / N

    else:
        # Si existen links (se calcula la distribución de prob)
        # Probabilidad de pagina aleatoria 
        prob_pag = no_damping_factor / N
        # Probabilidad de tomar link de la pagina
        prob_link = damping_factor / Num_Links

        for i in corpus.keys():
            if i in corpus[page]:
                distribucion_probabilidades[i] = prob_pag + prob_link
            else:
                distribucion_probabilidades[i] = prob_pag
        
    return distribucion_probabilidades



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
# basados en las instrucciones 
## You may assume that n will be at least 1.
# donde asumimos que n es al menos 1
    if n > 0:
        # diccionario de Return con estimado de cada PageRank
        valor_page_rank = {}
        
        # listado de todas las paginas
        paginas_todas = list(corpus.keys())

        # Para cada pagina un valor inicial de cero
        # asegurarnos que cada elemento tenga un valor inicial
        for pagina in corpus:
            valor_page_rank[pagina] = 0

        # donde nos piden que 
        ## The first sample should be generated by choosing from a page at random.
        muestra = random.choice(paginas_todas)
        valor_page_rank[muestra] +=1
        # muestreo de n-1 dado que la primera muestra ya fue generada
        for i in range(n-1):
            # a partir de la primera muestra generada aleatoriamente
            # el resto de las muestras son generadas basadas en el modelo de transición
            modelo = transition_model(corpus, muestra, damping_factor)
            muestra = random.choices(list(modelo.keys()), list(modelo.values()), k = 1)[0]
            # k=1 para que random.choices tome solo un elemento
            valor_page_rank[muestra] +=1

        # Normalizando el resultado
        for pagina in valor_page_rank:
            valor_page_rank[pagina]/=n
        
        return valor_page_rank
    
    else:
        raise ValueError("EPA! Mosca mi rey, la muestra debe ser mayor 0 papi")




def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Número de paginas (definido como en la función Transition Model)
    N = len(corpus)
    # Diccionario que va a guardar PageRanks de cada pagina
    ranks = {}
    # valores de PageRank iniciales a partir de la instrucción
    ## The function should begin by assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.
    for pagina in corpus:
        ranks[pagina] = 1/N
        
    # basado en la instrucción la función:
    # should accept a corpus of web pages and a damping factor
    # calculate PageRanks based on the iteration formula described above
    # and return each page’s PageRank accurate to within 0.001.
    convergencia = 0.001

    while True:
        nuevos_ranks = {}
        # para la contribución total del rank de cada pagina
        for pagina in corpus:
            # variable que acumule el rank total de otras paginas que se enlazan a la pagina actual
            suma_contribucion = 0

            for i in corpus:
                # lista de paginas enlazadas a i
                paginas_enlazadas = corpus[i]
                # condicional que ve si:
                # la pagina actual es de las que se i enlaza
                # si i no tiene ningún enlace saliente
                if pagina in paginas_enlazadas or not paginas_enlazadas:
                    # para determinar el numero de links si i no esta vacia entonces i tiene links (en particular len(paginas enlazadas) )
                    # en otro caso es N, el numero total de paginas incluida ella misma.
                    conteo_links = len(paginas_enlazadas) if paginas_enlazadas else N
                    # sumatorio del algoritmo
                    suma_contribucion += ranks[i] / conteo_links
            # funcion del algorimo PR(p) p = i, usando la notación de esta función        
            funcion_algoritmo = (1-damping_factor) / N + damping_factor * suma_contribucion
            nuevos_ranks[pagina] = funcion_algoritmo

        
        # verificamos la convergencia
        if all(abs(nuevos_ranks[ pagina ]- ranks[pagina]) < convergencia for pagina in corpus):
            # frenamos el bucle infinito de while True
            break

        ranks = nuevos_ranks

    # Normalizando
    rank_total = sum(nuevos_ranks.values())

    rank_normalizados = {}
    
    for pagina, rank in nuevos_ranks.items():
        rank_normalizados[pagina] = rank / rank_total

    return rank_normalizados



if __name__ == "__main__":
    main()