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

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
"""
num_hours_i_spent_on_this_assignment = 30+
"""
#
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>
The course has been fairly interesting so far. I had a lot of difficulties
with the a* search algorithm. Some of the finer details of the algoritm
was missunderstood and caused a lot of headache for this assignment. For
changes, I would like going over a detailed implementation of minimax.

"""
#####################################################
#####################################################

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

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
    """
    Q1.1
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ( problem.getStartState() )
    You will get (5,5)

    print (problem.isGoalState(problem.getStartState()) )
    You will get True

    print ( problem.getSuccessors(problem.getStartState()) )
    You will get [((x1,y1),'South',1),((x2,y2),'West',1)]
    """
    "*** YOUR CODE HERE ***"
    from game import Directions

    fringe = util.Stack()
    start = problem.getStartState()
    startState = (start, [], [])
    # state = (x,y coordinate of node, array of path to node from start, array of visited nodes)
    fringe.push(startState)

    while not fringe.isEmpty():
        node = fringe.pop()
        coordinate = node[0]
        actions = node[1]
        visited = node[2]

        if problem.isGoalState(coordinate):
            return actions

        expand = problem.getSuccessors(coordinate)
        for sucNode,action,cost in expand:
            if not sucNode in visited:
                fringe.push((sucNode, actions + [action], visited + [sucNode]))

    return []




def breadthFirstSearch(problem):
    """
    Q1.2
    Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    

    fringe = util.Queue()
    visited = []
    start = problem.getStartState()
    startState = (start, [])
    # state = (xy coord of node, paths to node)
    fringe.push(startState)
    visited.append(start)

    while not fringe.isEmpty():
        node = fringe.pop()
        coordinate = node[0]
        actions = node[1]

        if problem.isGoalState(coordinate):
            return actions

        expand = problem.getSuccessors(coordinate)
        for i in expand:
            newCoordinate = i[0]
            newPath = i[1]
            if (not newCoordinate in visited):
                visited.append(newCoordinate)
                fringe.push((newCoordinate, actions + [newPath]))

    return []



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Q1.3
    Search the node that has the lowest combined cost and heuristic first."""
    """Call heuristic(s,problem) to get h(s) value."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue()
    visited = []
    start = problem.getStartState()
    startState = (start, [], 0)
    # state = ( x,y coordinates of node, paths taken, gCost)
    fringe.push(startState, heuristic(start,problem))

    while not fringe.isEmpty():
        prevnode = fringe.pop()
        coordinate = prevnode[0]
        actions = prevnode[1]
        prevGCosts = prevnode[2]

        
        if not coordinate in visited:
            visited.append(coordinate)
        
            if problem.isGoalState(coordinate):
                return actions

            expand = problem.getSuccessors(coordinate)

            for node,action,cost in expand:
                gCost = cost + prevGCosts
                fCost = gCost + heuristic(node, problem)
                fringe.push((node, actions + [action], gCost ), fCost)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
