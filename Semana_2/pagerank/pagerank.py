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
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
