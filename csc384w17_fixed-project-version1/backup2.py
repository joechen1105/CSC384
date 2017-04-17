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

import random, util, sys



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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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


        #util.raiseNotDefined()
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
            successorList.append(gameState.generateSuccessor(agentIndex, action))
        temp_list= []
        if (agentIndex == 0):
            for successor in successorList:
                temp_list.append(self.DFMinMax(successor, nextDepth, nextAgent))

            if depth == self.depth:
                return actions[temp_list.index(max(temp_list))]

            return max(temp_list)
        else:
            for successor in successorList:
                temp_list.append(self.DFMinMax(successor, nextDepth, nextAgent))
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
                    # if alpha purning happened, it is pacman's choice, store it
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
            successorList.append(gameState.generateSuccessor(agentIndex, action))

        temp_list= []
        if (agentIndex == 0):
            for successor in successorList:
                temp_list.append(self.Expectimax(successor, nextDepth, nextAgent))

            if depth == self.depth:
                return actions[temp_list.index(max(temp_list))]

            return max(temp_list)
        else:
            for successor in successorList:
                temp_list.append(self.Expectimax(successor, nextDepth, nextAgent))

            return (sum(temp_list)/len(temp_list))


#add the function scoreEvaluationFunction to multiAgents.py
def scoreEvaluationFunction(currentGameState):
   """
     This default evaluation function just returns the score of the state.
     The score is the same one displayed in the Pacman GUI.

     This evaluation function is meant for use with adversarial search agents
   """
   return currentGameState.getScore()






# add this class to multiAgents.py
# the following class corrects and replaces the previous MonteCarloAgent class released on March 19
# the only differences between this version, and the one released on March 19 are:
#       * line 37 of this file, "if self.Q" has been replaced by "if Q"
#       * line 45 of this file, where "assert( Q == 'contestClassic' )" has been added
class MonteCarloAgent(MultiAgentSearchAgent):
    """
        Your monte-carlo agent (question 5)
        ***UCT = MCTS + UBC1***
        TODO:
        1) Complete getAction to return the best action based on UCT.
        2) Complete run_simulation to simulate moves using UCT.
        3) Complete final, which updates the value of each of the states visited during a play of the game.

        * If you want to add more functions to further modularize your implementation, feel free to.
        * Make sure that your dictionaries are implemented in the following way:
            -> Keys are game states.
            -> Value are integers. When performing division (i.e. wins/plays) don't forget to convert to float.
      """

    def __init__(self, evalFn='mctsEvalFunction', depth='-1', timeout='50', numTraining=100, C='2', Q=None):
        # This is where you set C, the depth, and the evaluation function for the section "Enhancements for MCTS agent".
        if Q:
            if Q == 'minimaxClassic':
                pass
            elif Q == 'testClassic':
                pass
            elif Q == 'smallClassic':
                pass
            else: # Q == 'contestClassic'
                assert( Q == 'contestClassic' )
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
        self.N = 0
        self.calculation_time = datetime.timedelta(milliseconds=int(timeout))

        self.numTraining = numTraining

        "*** YOUR CODE HERE ***"
        self.children = dict()
        self.parent = dict()

        #self.actions = dict()

        MultiAgentSearchAgent.__init__(self, evalFn, depth)

        def update(self, state):
            """
            You do not need to modify this function. This function is called every time an agent makes a move.
            """
            self.states.append(state)

    def getAction(self, gameState):
        """
        Returns the best action using UCT. Calls run_simulation to update nodes
        in its wins and plays dictionary, and returns best successor of gameState.
        """
        "*** YOUR CODE HERE ***"
        self.N = 0
        begin = datetime.datetime.utcnow()
        action = None
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.N += 1


            self.run_simulation(gameState)

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
        self.initialize(gameState)

        if (not(self.children.has_key(gameState))):
            self.plays[gameState] = 0
            self.wins[gameState] = 0
            self.Expansion(gameState, 0)

        selected_node, selected_node_depth = self.Select(gameState)

        if (self.plays[selected_node] != 0):

            node_parent_index = (self.parent[selected_node])[1]

            if(node_parent_index < (selected_node.getNumAgents() - 1)):
                agentIndex = node_parent_index + 1
            else:
                agentIndex = 0

            self.Expansion(selected_node, agentIndex)

            node_after_expand, selected_node_depth = self.Select(gameState)

            node_parent_index = (self.parent[node_after_expand])[1]

            if(node_parent_index < (selected_node.getNumAgents() - 1)):
                agentIndex = node_parent_index + 1
            else:
                agentIndex = 0

            self.Simulation(node_after_expand, agentIndex, selected_node_depth, gameState)

        else:

            node_parent_index = (self.parent[selected_node])[1]

            if(node_parent_index < (selected_node.getNumAgents() - 1)):
                agentIndex = node_parent_index + 1
            else:
                agentIndex = 0

            self.Simulation(selected_node, agentIndex, selected_node_depth, gameState)


    def initialize(self, gameState):
        state_list = self.plays.keys()
        #cur_state = gameState
        agentIndex = 0

        i = len(state_list)

        state_queue = [gameState]
        cur_state = state_queue.pop(0)
        while (cur_state in state_list):
            actions = cur_state.getLegalActions(agentIndex)
            for action in actions:
                temp_state = cur_state.generateSuccessor(agentIndex, action)
                for state in state_list:
                    if (temp_state.__eq__(state)):
                        if (self.children.has_key(cur_state)):
                            self.children[cur_state].append(state)
                        else:
                            self.children[cur_state] = [state]
                        self.parent[state] = (cur_state, agentIndex)
                        state_queue.append(state)

            if (len(state_queue) == 0):
                break
            cur_state = state_queue.pop(0)
            agentIndex = (self.parent[cur_state])[1]

            if(agentIndex < (cur_state.getNumAgents() - 1)):
                agentIndex += 1
            else:
                agentIndex = 0


    def Simulation(self, node, agentIndex, cur_depth, root):
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
            self.final(node, root, value)

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
            self.final(node, root, value)


    def Expansion(self, node, agentIndex):
        actions = node.getLegalActions(agentIndex)
        for action in actions:
            cur_node = node.generateSuccessor(agentIndex, action)
            if (self.children.has_key(node)):
                self.children[node].append(cur_node)
            else:
                self.children[node] = [cur_node]

            self.parent[cur_node] = (node, agentIndex)

            self.plays[cur_node] = 0
            self.wins[cur_node] = 0


    def Select(self, gameState):
        cur_node = gameState
        inf_detected = False

        cur_node_depth = 0
        while(self.children.has_key(cur_node)):
            children = self.children[cur_node]

            UCB_list = []
            children_list = []

            for child in children:

                children_list.append(child)

                if (self.plays[child] == 0):
                    cur_node = child
                    inf_detected = True
                    cur_UCB = sys.maxint
                    UCB_list.append(cur_UCB)
                    break
                else:
                    if (self.N == 0):
                        cur_UCB = 0
                    else:
                        cur_UCB = self.UCB1(self.wins[child], self.C, self.N, self.plays[child])

                UCB_list.append(cur_UCB)


            cur_node = children_list[UCB_list.index(max(UCB_list))]

            if (inf_detected):
                break
            cur_node_depth += 1


        return cur_node, cur_node_depth


    def final(self, state, root, value):
        """
        Called by Pacman game at the terminal state.
        Updates search tree values of states that were visited during an actual game of pacman.
        """
        "*** YOUR CODE HERE ***"

        cur_node = state
        self.plays[cur_node] += 1
        self.wins[cur_node] += value

        self.wins[root] += value

        while (self.parent.has_key(cur_node)):
            cur_node = (self.parent[cur_node])[0]
            if(cur_node.__eq__(root)):
                break
            self.plays[cur_node] += 1
            self.wins[cur_node] += value





    def findBestAction(self, gameState):
        temp_list= []

        actions = gameState.getLegalActions(0)

        for i in range(len(actions)):
            child = self.children[gameState][i]
            vi = self.wins[child]
            ni = self.plays[child]
            if (self.wins.has_key(child) and self.plays.has_key(child) and (ni != 0)):
                temp_list.append(float(vi)/float(ni))
            else:
                temp_list.append(sys.maxint)
        temp_list = temp_list[:len(actions)]
        return actions[temp_list.index(max(temp_list))]

    def UCB1(self, vi, C, N, ni):
        #UCB = float(vi + (C * (math.sqrt((math.log(N))/ni))))
        a = math.log(N)
        b = a/ni
        d = math.sqrt(b)
        e = float(C) * d
        UCB = float(e) + float(vi)/float(ni)
        return UCB

def mctsEvalFunction(state):
    """
    Evaluates state reached at the end of the expansion phase.
    """
    return 1 if state.isWin() else 0

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (to help improve your UCT MCTS).
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
