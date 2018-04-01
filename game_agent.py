"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return weight_heuristic_steps(game, player)

def weight_heuristic_steps(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    moves = len(game.get_legal_moves(player))
    prob_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return moves * moves - 1.5 * prob_moves * prob_moves


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return weight_heuristic_steps2(game, player)

def weight_heuristic_steps2(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return 1.5 * moves * moves - opponent_moves * opponent_moves

def weight_heuristic_steps3(game, player):

    opponent = game.get_opponent(player)
    opponent_moves = game.get_legal_moves(opponent)
    p_moves = game.get_legal_moves()
    common_moves = opponent_moves and p_moves

    if not opponent_moves:
        return float("inf")
    if not p_moves:
        return float("-inf")

    move_convergence = 1 / (game.move_count + 1)
    inverse_convergence = 1 / move_convergence
    return float(len(common_moves) * move_convergence + inverse_convergence * len(game.get_legal_moves()))

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return weight_heuristic_steps3(game, player)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def check_time(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
    
    def is_terminate(self, game, depth):
        """Helper method to check if we've reached the end of the game tree or
        if the maximum depth has been reached.
        """
        self.check_time()
        if len(game.get_legal_moves()) != 0 and depth > 0:
            return False
        return True

    def max_value(self, game, depth):
        self.check_time()
        if self.is_terminate(game, depth):
            return self.score(game, self)
        max_val = float("-inf")
        moves = game.get_legal_moves()
        for move in moves:
            forecast = game.forecast_move(move)
            max_val = max(max_val, self.min_value(forecast, depth - 1))
        return max_val

    def min_value(self, game, depth):
        self.check_time()
        if self.is_terminate(game, depth):
            return self.score(game, self)
        min_val = float("inf")
        legal_moves = game.get_legal_moves()
        for move in legal_moves:
            forecast = game.forecast_move(move)
            min_val = min(min_val, self.max_value(forecast, depth - 1))
        return min_val

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        # TODO: finish this function!
        self.check_time()
        moves = game.get_legal_moves()
        if not moves:
            return (-1, -1)
        values = [(self.min_value(game.forecast_move(m), depth - 1), m) for m in moves]
        _, move = max(values)
        return move

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    def check_time(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        move = (-1, -1)
        for i in range(1, 10000):
            try:
                move = self.alphabeta(game, i)
            except SearchTimeout:

                break
        return move
    
    def min_value(self, game, depth, alpha, beta):
        self.check_time()
        best_move = (-1, -1)
        if self.is_terminate(game, depth):
            return (self.score(game, self), best_move)
        value = float("inf")
        legal_moves = game.get_legal_moves()
        for move in legal_moves:
            result = self.max_value(game.forecast_move(move), depth - 1, alpha, beta)
            if result[0] < value:
                value, _ = result
                best_move = move
            if value <= alpha:
                return (value, best_move)
            beta = min(beta, value)
        return (value, best_move)

    def is_terminate(self, game, depth):
        self.check_time()
        if len(game.get_legal_moves()) != 0 and depth > 0:
            return False
        return True

    def max_value(self, game, depth, alpha, beta):
        self.check_time()
        best_move = (-1, -1)
        if self.is_terminate(game, depth):
            return (self.score(game, self), best_move)
        value = float("-inf")
        legal_moves = game.get_legal_moves()
        for move in legal_moves:
            result = self.min_value(game.forecast_move(move), depth - 1, alpha, beta)
            if result[0] > value:
                value, _ = result
                best_move = move
            if value >= beta:
                return (value, best_move)
            alpha = max(alpha, value)
        return (value, best_move)

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        # TODO: finish this function!
        self.check_time()
        _,move = self.max_value(game, depth, alpha, beta)
        return move
     
