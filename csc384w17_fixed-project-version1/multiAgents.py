# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
from operator import itemgetter
import math
# add this import to the header of multiAgents.py
import datetime

import random
import util
import sys


from game import Agent


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        # util.raiseNotDefined()
        temp = self.depth
        return (self.DFMinMax(gameState, temp, 0))

    def DFMinMax(self, gameState, depth, agentIndex):
        if (depth == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if(agentIndex < (gameState.getNumAgents() - 1)):
            nextDepth = depth
            nextAgent = agentIndex + 1
        else:
            nextDepth = depth - 1
            nextAgent = 0

        successorList = []
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successorList.append(
                gameState.generateSuccessor(agentIndex, action))
        temp_list = []
        if (agentIndex == 0):
            for successor in successorList:
                temp_list.append(self.DFMinMax(
                    successor, nextDepth, nextAgent))

            if depth == self.depth:
                return actions[temp_list.index(max(temp_list))]

            return max(temp_list)
        else:
            for successor in successorList:
                temp_list.append(self.DFMinMax(
                    successor, nextDepth, nextAgent))
            return min(temp_list)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.AlphaBeta(gameState, self.depth, 0, -sys.maxint, sys.maxint)

    def AlphaBeta(self, gameState, depth, agentIndex, alpha, beta):
        if (depth == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if(agentIndex < (gameState.getNumAgents() - 1)):
            nextDepth = depth
            nextAgent = agentIndex + 1
        else:
            nextDepth = depth - 1
            nextAgent = 0

        actions = gameState.getLegalActions(agentIndex)

        # variable that stores the action took when alpha purning happens
        alpha_action = None
        if (agentIndex == 0):
            for action in actions:
                cur_alpha = self.AlphaBeta(gameState.generateSuccessor(agentIndex, action),
                                                    nextDepth, nextAgent, alpha, beta)
                if (cur_alpha > alpha):
                    alpha = cur_alpha
                    # if alpha purning happened, it is pacman's choice, store
                    # it
                    alpha_action = action
                if beta <= alpha:
                    break
            # program recursed to its topped level
            # return the last purning action
            if (depth == self.depth):
                return alpha_action
            return alpha
        else:
            for action in actions:
                beta = min(beta, self.AlphaBeta(gameState.generateSuccessor(agentIndex, action),
                                                    nextDepth, nextAgent, alpha, beta))
                if beta <= alpha:
                    break
            return beta


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.Expectimax(gameState, self.depth, self.index)

    def Expectimax(self, gameState, depth, agentIndex):
        if (depth == 0) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if(agentIndex < (gameState.getNumAgents() - 1)):
            nextDepth = depth
            nextAgent = agentIndex + 1
        else:
            nextDepth = depth - 1
            nextAgent = 0

        successorList = []
        actions = gameState.getLegalActions(agentIndex)
        for action in actions:
            successorList.append(
                gameState.generateSuccessor(agentIndex, action))

        temp_list = []
        if (agentIndex == 0):
            for successor in successorList:
                temp_list.append(self.Expectimax(
                    successor, nextDepth, nextAgent))

            if depth == self.depth:
                return actions[temp_list.index(max(temp_list))]

            return max(temp_list)
        else:
            for successor in successorList:
                temp_list.append(self.Expectimax(
                    successor, nextDepth, nextAgent))

            return (sum(temp_list) / len(temp_list))



# add the function scoreEvaluationFunction to multiAgents.py
def scoreEvaluationFunction(currentGameState):
   """
     This default evaluation function just returns the score of the state.
     The score is the same one displayed in the Pacman GUI.

     This evaluation function is meant for use with adversarial search agents
   """
   return currentGameState.getScore()


class MonteCarloAgent(MultiAgentSearchAgent):
    """
        Your monte-carlo agent (question 5)
        ***UCT = MCTS + UBC1***
        TODO:
        1) Complete getAction to return the best action based on UCT.
        2) Complete runSimulation to simulate moves using UCT.
        3) Complete final, which updates the value of each of the states visited during a play of the game.

        * If you want to add more functions to further modularize your implementation, feel free to.
        * Make sure that your dictionaries are implemented in the following way:
            -> Keys are game states.
            -> Value are integers. When performing division (i.e. wins/plays) don't forget to convert to float.
      """

    def __init__(self, evalFn='mctsEvalFunction', depth='-1', timeout='50', numTraining=100, C='2', Q=None):
        # This is where you set C, the depth, and the evaluation function for the
        # section "Enhancements for MCTS agent".
        if Q:
            if Q == 'minimaxClassic':
                self.C = 1
                pass
            elif Q == 'testClassic':
                pass
            elif Q == 'smallClassic':
                pass
            else:  # Q == 'contestClassic'
                assert(Q == 'contestClassic')
                pass
        # Otherwise, your agent will default to these values.
        else:
            self.C = int(C)
            # If using depth-limited UCT, need to set a heuristic evaluation function.
            if int(depth) > 0:
                evalFn = 'scoreEvaluationFunction'
        self.states = []
        self.plays = dict()
        self.wins = dict()
        self.calculation_time = datetime.timedelta(milliseconds=int(timeout))

        self.numTraining = numTraining

        "*** YOUR CODE HERE ***"

        MultiAgentSearchAgent.__init__(self, evalFn, depth)

    def update(self, state):
        """
        You do not need to modify this function. This function is called every time an agent makes a move.
        """
        self.states.append(state)

    def getAction(self, gameState):
        """
        Returns the best action using UCT. Calls runSimulation to update nodes
        in its wins and plays dictionary, and returns best successor of gameState.
        """
        "*** YOUR CODE HERE ***"
        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation(gameState)
            games += 1

        action = self.findBestAction(gameState)
        return action

    def run_simulation(self, gameState):
        """
        Simulates moves based on MCTS.
        1) (Selection) While not at a leaf node, traverse tree using UCB1.
        2) (Expansion) When reach a leaf node, expand.
        4) (Simulation) Select random moves until terminal state is reached.
        3) (Backpropapgation) Update all nodes visited in search tree with appropriate values.
        * Remember to limit the depth of the search only in the expansion phase!
        Updates values of appropriate states in search with with evaluation function.
        """
        "*** YOUR CODE HERE ***"
        # if initial tree is not given
        if(len(self.plays) == 0):
            self.plays[gameState] = 1
            self.wins[gameState] = self.simulation(gameState, self.depth, self.index)
        # if there is a given tree
        else:
            visited_nodes = [gameState]
            cur_node = gameState
            level_nodes = []
            agentIndex = 0
            try:
                self.plays[cur_node]
            except:
                self.plays[cur_node] = 0
                self.wins[cur_node] = 0
            while(True):
                if(self.plays[cur_node] == 0):
                    self.update_values(visited_nodes, cur_node, self.depth, agentIndex)
                    break
                level_nodes = [cur_node.generateSuccessor(
                    agentIndex, a) for a in cur_node.getLegalActions(agentIndex)]
                actions = cur_node.getLegalActions(agentIndex)
                for action in actions:
                    level_nodes.append(cur_node.generateSuccessor(agentIndex, action))
                if(len(level_nodes) == 0):
                    break
                try:
                    for node in level_nodes:
                        self.plays[node]
                except:
                    for node in level_nodes:
                        if (node not in self.plays.keys()):
                            self.plays[node] = 0
                            self.wins[node] = 0

                intersect_nodes = [node for node in level_nodes if node in self.plays.keys()]
                if (not intersect_nodes):
                    cur_node = level_nodes[0]
                    visited_nodes.append(cur_node)
                    for node in level_nodes:
                        self.Expansion(node, agentIndex)
                    update_values(visited_nodes, cur_node, self.depth, agentIndex)
                    break
                else:
                    UCB_list = []

                    for node in level_nodes:
                        if (self.plays[node] != 0):
                            vi = float(self.wins[node])/float(self.plays[node])
                            UCB_list.append(self.UCB1(vi, self.C, self.plays[cur_node], self.plays[node]))
                        else:
                            UCB_list.append(sys.maxint)
                    cur_node = level_nodes[UCB_list.index(max(UCB_list))]
                    visited_nodes.append(cur_node)
                if(agentIndex < (gameState.getNumAgents() - 1)):
                    agentIndex += 1
                else:
                    agentIndex = 0

    def UCB1(self, vi, C, N, ni):
        a = math.log(N)
        b = float(a)/float(ni)
        d = math.sqrt(b)
        e = float(C) * d
        UCB = float(e) + vi
        #print UCB
        return UCB

    def update_values(self, visited_nodes, cur_node, depth, agentIndex):
        value = self.simulation(cur_node, depth, agentIndex)
        for node in visited_nodes:
            self.plays[node] += 1
            self.wins[node] += value

    def Expansion(self, node, agentIndex):
        actions = node.getLegalActions(agentIndex)
        for action in actions:
            cur_node = node.generateSuccessor(agentIndex, action)
            self.plays[cur_node] = 0
            self.wins[cur_node] = 0

    def final(self, state):
        """
        Called by Pacman game at the terminal state.
        Updates search tree values of states that were visited during an actual game of pacman.
        """
        "*** YOUR CODE HERE ***"
        pass

    def simulation(self, node, cur_depth, agentIndex):
        cur_node = node
        cur_agent = agentIndex
        if(self.depth < 0):
            while (not(cur_node.isWin() or cur_node.isLose())):
                actions = cur_node.getLegalActions(cur_agent)
                random_action = random.choice(actions)
                random_node = cur_node.generateSuccessor(cur_agent, random_action)
                cur_node = random_node
                if(cur_agent < (cur_node.getNumAgents() - 1)):
                        cur_agent += 1
                else:
                        cur_agent = 0
            value = self.evaluationFunction(cur_node)
        else:
            remaining_depth = self.depth - cur_depth + 1
            while (not(cur_node.isWin() or cur_node.isLose())):
                if (remaining_depth == 0):
                    break
                actions = cur_node.getLegalActions(cur_agent)
                random_action = random.choice(actions)
                random_node = cur_node.generateSuccessor(cur_agent, random_action)
                if(cur_agent < (cur_node.getNumAgents() - 1)):
                    cur_agent += 1
                else:
                    cur_agent = 0
                remaining_depth -= 1
            value = self.evaluationFunction(cur_node)
        return value

    def findBestAction(self, gameState):
        temp_list= []
        actions = gameState.getLegalActions(0)

        for action in actions:
            child = gameState.generateSuccessor(0, action)
            if (self.wins.has_key(child) and self.plays.has_key(child) and (self.plays[child] != 0)):
                vi = float(self.wins[child])/float(self.plays[child])
                temp_list.append(vi)
            else:
                temp_list.append(sys.maxint)
        return actions[temp_list.index(max(temp_list))]

def mctsEvalFunction(state):
    """
    Evaluates state reached at the end of the expansion phase.
    """
    return 1 if state.isWin() else 0

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
