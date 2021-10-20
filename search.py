# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from game import Directions
import time
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    "get start state and save start state as current state"
    currentstate = problem.getStartState()

    "make explored list and add start to it"
    explored = [problem.getStartState()]

    "create our stack"
    stack = util.Stack()

    "check type of data -> tuple"
    print("TYPE OF ---------------------:",type(problem.getStartState()))

    "temporary tuple to push to stack"
    tuplehold = (problem.getStartState(), [])
    stack.push(tuplehold)

    while not problem.isGoalState(currentstate):

        "Get top state from stack and add it to paths list, also change current state"
        "also take the path associated to this node"
        cState, directions = stack.pop()
        "add current working state to explored list"
        explored.append(cState)

        "get next possible nodes from current state"
        next = problem.getSuccessors(cState)
        print(next)
        "check for each leaf of this node is this leaf has been explored yet"
        for i in next:
            "check first element (location) of next options and see if it has been visited yet"
            nextpos = i[0]
            if not nextpos in explored:
                "move to next node in list"
                currentstate = i[0]
                "add direction directions to this node and push this to the stack"
                stack.push((nextpos, directions + [i[1]]))

    "We exit when goal state is reached, that means last position was goal and the last set of directions are okay"
    cState, directions = stack.pop()
    return directions


def breadthFirstSearch(problem):
    "get start state and save start state as current state"
    currentstate = problem.getStartState()
    "make explored list and add start to it"
    explored = [problem.getStartState()]
    "create our stack"
    Queue = util.Queue()
    "check type of data -> tuple"
    print("TYPE OF ---------------------:",type(problem.getStartState()))
    "temporary tuple to push to stack"
    tuplehold = (problem.getStartState(), [])
    Queue.push(tuplehold)
    directions = []
    while not problem.isGoalState(currentstate):
        "Get top state from Q and add it to paths list, also change current state"
        "also take the path associated to this node"
        cState, directions = Queue.pop()        
        if problem.isGoalState(cState):
            return directions 
        "add current working state to explored list"
        explored.append(cState)
        "get next possible nodes from current state"
        next = problem.getSuccessors(cState)
        "check for each leaf of this node is this leaf has been explored yet"
        for i in next:
            "check first element (location) of next options and see if it has been visited yet"
            nextpos = i[0]
            if not nextpos in explored:
                explored.append(nextpos)
                "add direction directions to this node and push this to the Q"
                Queue.push((nextpos, directions + [i[1]]))
    "We exit when goal state is reached, that means last position was goal and the last set of directions are okay"
    return directions

def uniformCostSearch(problem):
    explored = []
    "create our stack"
    Queue = util.PriorityQueue()
    
    "check type of data -> tuple"
    print("TYPE OF ---------------------:",type(problem.getStartState()))
    "temporary tuple to push to stack"
    tuplehold = (problem.getStartState(), [])
    Queue.push(tuplehold,0)
    directions = []
    while not Queue.isEmpty():
        "Get top state from Q and add it to paths list, also change current state"
        "also take the path associated to this node"
        cState, directions = Queue.pop()
        if problem.isGoalState(cState):
            return directions 
       
        "check for each leaf of this node is this leaf has been explored yet"
        if cState not in explored:
            "add current working state to explored list"
            explored.append(cState)
            "get next possible nodes from current state"
            next = problem.getSuccessors(cState)
            for i in next:
                "check first element (location) of next options and see if it has been visited yet"
                nextpos = i[0]
                if nextpos not in explored:
                    "add direction directions to this node and push this to the Q"
                    Queue.update((nextpos, directions + [i[1]]),problem.getCostOfActions(directions + [i[1]]))
                
        
    "We exit when goal state is reached, that means last position was goal and the last set of directions are okay"
    return directions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
