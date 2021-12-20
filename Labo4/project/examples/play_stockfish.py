#!/usr/bin/python3
#from ..chess_utilities.example_utility import ExampleUtility
#from ..chess_agents.example_agent import ExampleAgent
#from ..chess_agents.Carlo import Carlo
import chess
import chess.engine
import chess.pgn
import math
import random
import numpy as np
import time




"""A generic agent class"""

class Carlo():

    def __init__(self) -> None:
        """Setup the Search Agent"""
        self.name = "CarloBot"
        self.state = chess.Board()
        self.action = ''
        self.children = set([])
        self.parent = None
        self.ParentN = 0
        self.N = 0
        self.v = 0
    
    def perform(board : chess.Board, ):
        pass
        
   
   
def UCB1(CurrentCarlo: Carlo):
        return  CurrentCarlo.v+2*(math.sqrt(math.log(CurrentCarlo.ParentN+math.e+(10**-6))/(CurrentCarlo.N+(10**-10))))
   
def expansion(CurrentCarlo : Carlo, white : bool):
    if(len(CurrentCarlo.children) == 0):
        return CurrentCarlo
    
    if white:
        highest = -69000000
        car = None
        for child in CurrentCarlo.children:
            UCB = UCB1(child)
            if(UCB > highest):
                highest = UCB
                car = child
        return (expansion(car,0))
    else:
        highest = 69000000
        car = None
        for child in CurrentCarlo.children:
            UCB = UCB1(child)
            if(UCB < highest):
                highest = UCB
                car = child
        return (expansion(car,1))

def calc(CurrentCarlo: Carlo):
    if(CurrentCarlo.state.is_game_over()):
        b = CurrentCarlo.state
        if(b.result()=='1-0'):
            return (1,CurrentCarlo)
        elif(b.result()=='0-1'):
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

def backprop(CurrentCarlo: Carlo,reward):
        CurrentCarlo.N+=1
        CurrentCarlo.v+= reward
        while(CurrentCarlo.parent != None):
            CurrentCarlo.ParentN += 1
            CurrentCarlo = CurrentCarlo.parent
        
        return CurrentCarlo

def mcts_pred(CurrentCarlo : Carlo ,GG : bool,white : bool,iterations=50):
    if(GG):
        return -1
    all_moves = [CurrentCarlo.state.san(i) for i in list(CurrentCarlo.state.legal_moves)]
    map_state_move = dict()
    
    for i in all_moves:
        istate = chess.Board(CurrentCarlo.state.fen())
        istate.push_san(i)
        miniCarlo = Carlo()
        miniCarlo.state = istate
        miniCarlo.parent = CurrentCarlo
        CurrentCarlo.children.add(miniCarlo)
        map_state_move[miniCarlo] = i
    
    while(iterations>0):
        if(white):  
            max_ucb = -69000000
            selectedCarlo = None
            for i in CurrentCarlo.children:
                ucb = UCB1(i)
                if(ucb>max_ucb):
                    max_ucb = ucb
                    selectedCarlo = i
            ExpandedCarlo = expansion(selectedCarlo,0)
            reward,state = calc(ExpandedCarlo)
            CurrentCarlo = backprop(state,reward)
            iterations-=1
    else:
        min_ucb = 69000000
        selectedCarlo = None
        for i in CurrentCarlo.children:
            ucb = UCB1(i)
            if(ucb<min_ucb):
                min_ucb = ucb
                selectedCarlo = i
        ExpandedCarlo = expansion(selectedCarlo,1)
        reward,state = calc(ExpandedCarlo)
        CurrentCarlo = backprop(state,reward)
        iterations-=1
    if(white):
            
        max = -69000000
        selected_move = ''
        for i in (CurrentCarlo.children):
            ucb = UCB1(i)
            if(ucb>max):
                max = ucb
                selected_move = map_state_move[i]
        return selected_move
    else:
        max = 69000000
        selected_move = ''
        for i in (CurrentCarlo.children):
            ucb = UCB1(i)
            if(ucb<max):
                max = ucb
                selected_move = map_state_move[i]
        return selected_move       

     


        


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

            move = mcts_pred(root,board.is_game_over(),1)
            board.push_san(move)
            turn_white_player = False
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






