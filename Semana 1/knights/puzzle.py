from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Inicial dado en las instrucciones del proyecto
    Or(AKnight, AKnave), # Es solamente caballero o bribon
    Not(And(AKnight, AKnave)),  # No puede ser ambos al mismo tiempo
    Implication(AKnight, And(AKnight, AKnave)), # Sí es caballero --> Aknight AND Aknave son True
    Implication(AKnave, Not(And(AKnight, AKnave))) # Sí es Bribon --> Aknight AND Aknave son False
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Partimos de la misma base que no puede ser knight y knave al mismo tiempo solo uno de los dos
    # para ambos casos
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),  
    # Sí A dice que ambos son knaves las posibles implicaciones son:
    Implication(AKnight, And(AKnave, BKnave)), # A es un caballero dice la verdad (ambos son bribones)
    Implication(AKnave, Not(And(AKnave, BKnave))) # A es un bribon y esta mintiendo.
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #en este caso son 4 escenarios partiendo claro de que estos no pueden ser iguales
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),  

    # los escenarios que tenemos son, en base a lo que dice A y B:
    # para A: (We are the same kind) Ambos son bribones o ambos son caballeros
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))), # la tesis es verdadera al ser caballero
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))), # la tesis es falsa/negación al ser bribon

    # para B: (We are of different kinds)
    Implication(BKnight, Or(And(BKnight, AKnave), And(BKnave, AKnight))), # la tesis es verdadera si B es caballero
    Implication(BKnave, Not(Or(And(BKnight, AKnave), And(BKnave, AKnight)))) # la tesis es falsa/negación si es el bribon
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Partimos del conocimiento base de que no pueden ser ambos al mismo tiempo
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),  

    # De igual forma que con el Puzzle 2 para entender las implicaciones a realizar se puede ir por sentencias
    
    # Para A: A knight or a Knave:
    Implication(AKnight, Or(AKnight, AKnave)),  # Sí es A caballero dice la verdad y es o caballero o bribon
    Implication(AKnave, Not(Or(AKnight, AKnave))), # si A es bribon miente y no es ni caballero o bribon

    # Para B: A dijo que es bribon (A said 'I am a knave')
        # Se parte de asumir que B es caballero
    Implication(BKnight,
                # Donde A puede ser el caballero o el bribon y diga la verdad o mienta.
                 Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),

        # Para el caso de que B sea el bribon, (estaria hablando webonadas de A en ese caso)
    Implication(BKnave,
                # Donde A puede ser el caballero o el bribon
                Or(Implication(AKnight, Not(AKnave)), Implication(AKnave, AKnave))),

    # Para B: C es el Bribon (C is a knave)
    Implication(BKnight, CKnave), # de igual manera sí B es caballero C seria bribon
    Implication(BKnave, Not(CKnave)), # si B es el bribon C no es el caballero

    # Para C:
    Implication(CKnight, AKnight), # Sí C es un caballero, dice la verdad y A es caballero
    Implication(CKnave, Not(AKnight)) # Sí C es bribon, entonces A no es el caballero
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
