"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Contadores del turno de cada jugador (variables)
    contador_x = 0
    contador_o = 0
    # recorrido en el tablero para llevar conteo de los turnos de cada jugador
    for fila in range(len(board)):
        for celda in range(len(board[fila])):
            if board[fila][celda] == X:
                contador_x += 1
            elif board[fila][celda] == O:
                contador_o += 1
    # se decide el turno del jugador
    # usando la especificación del ejercicio:
         # In the initial game state, X gets the first move. Subsequently, the player alternates with each additional move. 
    if contador_x == contador_o:
        return X
    elif contador_x > contador_o:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Este caso es como la inversa del bucle anterior buscamos los valores EMPTY
    
    # Primero el conjunto de las acciones
    posibles_movimientos = set()

    for fila in range(len(board)):
        for celda in range(len(board[0])):
            if board[fila][celda] == EMPTY:
                posibles_movimientos.add((fila, celda))

    return posibles_movimientos


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Debemos validar que la acción de los jugadores son validas.

    if action not in actions(board):
        raise NameError("¡Epa!, ¡mosca hay pues manito!, esta acción no esta permitida rey")
    else:
        fila , celda = action
        copia_tablero = copy.deepcopy(board)        
        copia_tablero[fila][celda] = player(board)
        return copia_tablero

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if False:
        return None
    else:
        for jugador in (X,O):
            # los resultados ganadores pueden darse horizontalemente verticalmente o en sus diagonales
            for fila in range(len(board)):
                    if board[fila][0] ==jugador and board[fila][1] == jugador and board[fila][2] == jugador:
                        return jugador
                    
            for celda in range(len(board)):
                    if board[0][celda] == jugador and board[1][celda] == jugador and board[2][celda] == jugador:
                        return jugador
                    
            if board[0][0] == jugador and board[1][1] == jugador  and board[2][2] == jugador:
                    return jugador
            
            if board[0][2] == jugador and board[1][1] == jugador  and board[2][0] == jugador:
                    return jugador

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X: 
        return True
    if winner(board) == O:
        return True
    for fila in range(len(board)):
        for celda in range(len(board[fila])):
            if board[fila][celda] == EMPTY:
                return False    # dado que si hay todavia celdas "EMPTY" no es empate, el juego aún no termina.
    return True # si se pasa el bucle foor es un empate, lo que hace que este terminado


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # bastante directa la instrucción de que hacer acá
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # guiado del pseudocodigo de las notas de la lección y del libro

    def max_valor(board):
        mov_optimo = ()
        if terminal(board):
            return utility(board), mov_optimo
        else:
            v = -math.inf # de import math
            for accion in actions(board):
                valor_min = min_valor(result(board, accion))[0]
                if valor_min > v:
                    v = valor_min
                    mov_optimo = accion
            return v, mov_optimo
        
    def min_valor(board):
        mov_optimo = ()
        if terminal(board):
            return utility(board), mov_optimo
        else:
            v = math.inf
            for accion in actions(board):
                valor_max = max_valor(result(board, accion))[0]
                if valor_max < v:
                    v = valor_max
                    mov_optimo = accion
            return v, mov_optimo
        
    jugador = player(board)

    if terminal(board):
        return None
    
    if jugador == X:
        return max_valor(board)[1]
    else:
        return min_valor(board)[1]
