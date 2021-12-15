from abc import ABC
import chess
import math
import random
from project.chess_utilities.utility import Utility

"""A generic agent class"""

class Carlo():

    def __init__(self, utility: Utility, time_limit_move: float) -> None:
        """Setup the Search Agent"""
        self.utility = utility
        self.time_limit_move = time_limit_move
        self.state = chess.Board()
        self.children = None
        self.parent = set()
        self.ParentN = 0
        self.N = 0
        self.U = 0
        

    def calculate_move(self, board: chess.Board):
        pass
   
   
    def UCB1(CurrentCarlo : Carlo):
        return (CurrentCarlo.U/CurrentCarlo.N) + 1.5 * math.sqrt(log(CurrentCarlo.ParentN)/CurrentCarlo.N)
   
   
   
    def selection(CurrentCarlo : Carlo):
        highest = -69000000
        car = None
        for child in CurrentCarlo.children:
            UCB = UCB1(child)
            if(UCB > highest):
                highest = UCB
                car = child
        return car

    def expansion(CurrentCarlo : Carlo):
        if(len(CurrentCarlo.children) == 0):
            return CurrentCarlo
        highest = -69000000
        car = None
        for child in CurrentCarlo.children:
            UCB = UCB1(child)
            if(UCB > highest):
                highest = UCB
                car = child
        return car

    def calc(CurrentCarlo : Carlo):
        if(CurrentCarlo.state.is_game_over()):
            if(chess.Board.result()=='1-0'):
                return (1,CurrentCarlo)
            elif(chess.Board.result()=='0-1'):
                return(-1,CurrentCarlo)
            else:
                return(0.5,CurrentCarlo)
        moves = [CurrentCarlo.state.san(i) for i in list(CurrentCarlo.state.legal_moves)]  
        for i in moves:
            s = chess.Board(CurrentCarlo.state.fen())
            s.push_san(i)
            Carlochild = Carlo()
            Carlochild.state = s
            Carlochild.parent = CurrentCarlo
            CurrentCarlo.children.add(Carlochild)
        rnd = random.choice(list(CurrentCarlo.children))
        return calc(rnd)

    def backprop(CurrentCarlo : Carlo):
        CurrentCarlo.U+=1
        while(CurrentCarlo.parent != None):
            CurrentCarlo.U += 1
            CurrentCarlo = CurrentCarlo.parent
        
        return CurrentCarlo


        
