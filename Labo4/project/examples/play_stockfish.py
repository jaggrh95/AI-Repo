#!/usr/bin/python3
#from ..chess_utilities.example_utility import ExampleUtility
#from ..chess_agents.example_agent import ExampleAgent
#from ..chess_agents.Carlo import Carlo
from typing import Dict
import chess
import chess.engine
import chess.pgn
import math
import random
import numpy as np
import time
#import pandas as pd
#import cython


TTable : dict()
"""A generic agent class"""

class Carlo():
    def __init__(self) -> None:
        """Setup the Search Agent"""
        self.state = chess.Board()
        self.capt = 0
        self.action = ''
        self.children = []
        self.parent = None
        self.ParentN = 0 #times parent has been visited
        self.N = 0 #times visited
        self.v = 0 #times won
               

def weightedRNDIndex(total, UCB : np.array,white):
    A = []
    Weights = []
    if(np.all(UCB == UCB[0])):
        return random.randint(0,len(UCB)-1)
    for i in range(len(UCB)):
        A.append(UCB[i])
        Weights.append(UCB[i]/total)
    if white:
        index =  np.random.choice(UCB,1,Weights)  #get weighted choice
    else:
        index = np.random.choice(UCB,1,Weights.reverse)
    print(index)
    if(len(A) > 1):
        G = A.index(index[0])
    else:
        G = A
    return G


def UCB1(CurrentCarlo: Carlo):
    if(CurrentCarlo.N == 0):
            return 0 + CurrentCarlo.capt
    if ((CurrentCarlo.ParentN)/(CurrentCarlo.N) == 0):
        return  CurrentCarlo.v/(CurrentCarlo.N)
    else:
        return  CurrentCarlo.v/(CurrentCarlo.N) + CurrentCarlo.capt + 1.5  * math.sqrt(math.log(CurrentCarlo.ParentN)/(CurrentCarlo.N)) 
     
   
def expansion(CurrentCarlo : Carlo, white : bool, depthexp=100):
    if(len(CurrentCarlo.children) == 0 or depthexp == 0):
        return CurrentCarlo
    UCB = np.array([UCB1(xi) for xi in CurrentCarlo.children])
    Total = np.sum(UCB)
    WeightedIndex = weightedRNDIndex(Total,UCB,white)
    return (expansion(CurrentCarlo.children[int(WeightedIndex)], not white ,depthexp-1))


def calc(CurrentCarlo: Carlo, depthcalc = 30):
    if(CurrentCarlo.state.is_game_over() or depthcalc == 0):
        b = CurrentCarlo.state
        if(b.result()=='1-0'):
            return (1,CurrentCarlo)
        elif(b.result()=='0-1'):
            return(-1,CurrentCarlo)
        else:
            return(0.5,CurrentCarlo)
    
    moves = [CurrentCarlo.state.san(i) for i in list(CurrentCarlo.state.legal_moves)]  
    for i in range(len(moves)):
        s = chess.Board(CurrentCarlo.state.fen())
        s.push_san(moves[i])
        Carlochild = Carlo()
        Carlochild.state = s
        Carlochild.parent = CurrentCarlo
        CurrentCarlo.children.append(Carlochild)
    return calc(random.choice(list(CurrentCarlo.children)),depthcalc-1)

def backprop(CurrentCarlo: Carlo,reward):
        CurrentCarlo.N +=1
        if(reward == 1):
            CurrentCarlo.v+= reward
        while(CurrentCarlo.parent != None):
            CurrentCarlo.ParentN += 1
            CurrentCarlo = CurrentCarlo.parent
            CurrentCarlo.N +=1
            if(reward == 1):
                CurrentCarlo.v+= reward
        return CurrentCarlo

def Monte(CurrentCarlo : Carlo ,GG : bool,white : bool,iterations=30):
    if(GG):
        return -1
    moves = dict()
    for i in list(CurrentCarlo.state.legal_moves):
        A = CurrentCarlo.state.san(i)
        istate = chess.Board(CurrentCarlo.state.fen())
        nr1 = str(i)[1]
        nr2 = str(i)[3]
        if(white):
            if(int(nr1) > int(nr2) and int(nr1) <=4 and (not chess.Board.is_capture(istate,i))):
                continue
        else:
            if(int(nr1) < int(nr2) and int(nr1) >=4 (not chess.Board.is_capture(istate,i))):
                continue
        istate.push_san(A)
        miniCarlo = Carlo()
        if(chess.Board.is_capture(chess.Board(CurrentCarlo.state.fen()),i)):
            miniCarlo.capt = 0.8
        miniCarlo.state = istate
        miniCarlo.parent = CurrentCarlo
        CurrentCarlo.children.append(miniCarlo)
        moves[miniCarlo] = A
    
        

    while(iterations>0):
        print(iterations)
        UCB = np.array([UCB1(xi) for xi in CurrentCarlo.children])
        if(white):  
            if(np.all(UCB == UCB[0])):
                ExpandedCarlo = expansion(random.choice(CurrentCarlo.children),0)
                reward,state = calc(ExpandedCarlo)
                CurrentCarlo = backprop(state,reward)
            else:
                index = weightedRNDIndex(np.sum(UCB),UCB,1)
                ExpandedCarlo = expansion(CurrentCarlo.children[index],0)
                reward,state = calc(ExpandedCarlo)
                CurrentCarlo = backprop(state,reward)
        else:
            if(np.all(UCB == UCB[0])):
                ExpandedCarlo = expansion(random.choice(CurrentCarlo.children),1)
                reward,state = calc(ExpandedCarlo)
                CurrentCarlo = backprop(state,reward)
            else:
                index = weightedRNDIndex(np.sum(UCB),UCB,0)
                ExpandedCarlo = expansion(CurrentCarlo.children[index],1)
                reward,state = calc(ExpandedCarlo)
                CurrentCarlo = backprop(state,reward)
        
        
        iterations-=1
    Weight = list()
    UCB = list()
    for CarloChild in CurrentCarlo.children:
        if(CarloChild.N == 0 and CarloChild.v == 0):
            Weight.append(0.0)
        else:
            Weight.append(CarloChild.v / (CarloChild.N))
        
        UCB.append(UCB1(CarloChild))

    print(UCB)
    if(white):
        if(Weight.count(Weight[0]) == len(Weight)):
            return moves[CurrentCarlo.children[np.argmax(UCB)]]
        return moves[CurrentCarlo.children[np.argmax(Weight)]]
    else:
        if(Weight.count(Weight[0]) == len(Weight)):
            return moves[CurrentCarlo.children[np.argmin(UCB)]]
        return moves[CurrentCarlo.children[np.argmin(Weight)]]

     


        


""" An agent plays a game against the stockfish engine """
def play_stockfish():
    
    time_limit = 5.0
        
    # Setup
    board = chess.Board()
    # Define agent here
    #white_player = ExampleAgent(ExampleUtility(), 5.0)

    
    
    # Enter your path here:
    black_player = chess.engine.SimpleEngine.popen_uci("C:/stockfish_14.1_win_x64_avx2/stockfish_14.1_win_x64_avx2.exe")
    # Determine the skill level of Stockfish:
    black_player.configure({"Skill Level": 1})
    limit = chess.engine.Limit(time=time_limit)
    running = True
    turn_white_player = True

    # Game loop
    while running:
        move = None

        if turn_white_player:
            # White plays a random move
            #move = white_player.calculate_move(board)
            root = Carlo()
            root.state = board

            move = Monte(root,board.is_game_over(),1)
            board.push_san(move)
            turn_white_player = False
            print(move)
            print("White plays")
        else:
            # Stockfish plays a move
            move = black_player.play(board, limit).move
            turn_white_player = True
            print("Black plays")
            board.push(move)

        
        print(board)
        print("----------------------------------------")
        
        # Check if a player has won
        if board.is_checkmate():
            running = False
            if turn_white_player:
                print("Stockfish wins!")
            else:
                print("{} wins!".format(root.name))

        # Check for draws
        if board.is_stalemate():
            running = False
            print("Draw by stalemate")
        elif board.is_insufficient_material():
            running = False
            print("Draw by insufficient material")
        elif board.is_fivefold_repetition():
            running = False
            print("Draw by fivefold repitition!")
        elif board.is_seventyfive_moves():
            running = False
            print("Draw by 75-moves rule")

    black_player.quit()
    return board

def main():
    play_stockfish()

if __name__ == "__main__":
    main()






