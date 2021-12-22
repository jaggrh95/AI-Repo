from abc import ABC
import chess
import math
from project.chess_utilities.utility import Utility

"""A generic agent class"""

class Carlo(ABC):

    def __init__(self, utility: Utility, time_limit_move: float) -> None:
        """Setup the Search Agent"""
        self.utility = utility
        self.time_limit_move = time_limit_move
        self.state = chess.Board()
        self.children = None
        self.parent = set()
        self.N = 0
        self.U = 0

    def calculate_move(self, board: chess.Board):
        pass
    def UCB1(CurrentCarlo : Carlo):
        return (CurrentCarlo.U/CurrentCarlo.N) + 1.5 * math.sqrt(log(CurrentCarlo.parent))
        
