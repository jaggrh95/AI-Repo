#!/usr/bin/python3
#from ..chess_utilities.example_utility import ExampleUtility
#from ..chess_agents.example_agent import ExampleAgent
#from ..chess_agents.Carlo import Carlo
import chess
import chess.engine
import chess.pgn
import math
import random
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

def rollout(CurrentCarlo: Carlo):
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
    return rollout(rnd)

def backprop(CurrentCarlo: Carlo,reward):
        CurrentCarlo.N+=1
        CurrentCarlo.v+= reward
        while(CurrentCarlo.parent != None):
            CurrentCarlo.ParentN += 1
            CurrentCarlo = CurrentCarlo.parent
        return CurrentCarlo

def mcts_pred(CurrentCarlo : Carlo ,GG : bool,white : bool,iterations=10):
    if(GG):
        return -1
    all_moves = [CurrentCarlo.state.san(i) for i in list(CurrentCarlo.state.legal_moves)]
    map_state_move = dict()
    
    for i in all_moves:
        tmp_state = chess.Board(CurrentCarlo.state.fen())
        tmp_state.push_san(i)
        child = Carlo()
        child.state = tmp_state
        child.parent = CurrentCarlo
        CurrentCarlo.children.add(child)
        map_state_move[child] = i
    
    while(iterations>0):
        if(white):  
            max_ucb = -69000000
            sel_child = None
            for i in CurrentCarlo.children:
                ucb = UCB1(i)
                if(ucb>max_ucb):
                    max_ucb = ucb
                    sel_child = i
            ex_child = expansion(sel_child,0)
            reward,state = rollout(ex_child)
            CurrentCarlo = backprop(state,reward)
            iterations-=1
    else:
        min_ucb = 69000000
        sel_child = None
        for i in CurrentCarlo.children:
            ucb = UCB1(i)
            if(ucb<min_ucb):
                min_ucb = ucb
                sel_child = i
        ex_child = expansion(sel_child,1)
        reward,state = rollout(ex_child)
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

     

