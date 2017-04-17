#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Sokoban warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
import os
from search import * #for search engines
from sokoban import SokobanState, Direction, PROBLEMS, sokoban_goal_state #for Sokoban specific classes and problems

import numpy as np
import scipy as sp
import math


#SOKOBAN HEURISTICS
def heur_displaced(state):
  '''trivial admissible sokoban heuristic'''
  '''INPUT: a sokoban state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  count = 0
  for box in state.boxes:
    if box not in state.storage:
      count += 1
  return count

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum Manhattan distance of the boxes to their closest storage spaces is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid and that several boxes can fit in one storage bin.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    
    # get box and storage cordinates
    box_cor = state.boxes.keys()
    stor_cor = state.storage.keys()
    
    box_dict = state.boxes
    ans_list = []
    
    # loop through all boxes with respecting to all storages
    for box in box_cor:
        temp_list = []
        i = box_dict[box]
        for storge in stor_cor:
            if(state.restrictions == None or storge in state.restrictions[i]):
                dist = abs(box[0] - storge[0]) + abs(box[1] - storge[1])
                temp_list.append(dist)
            else:
                temp_list.append(float('inf'))
        ans_list.append(temp_list)

    # calculating the sum with minimum value
    ans = np.sum(np.amin(ans_list,1))
    return ans

def heur_alternate(state):
#IMPLEMENT
    '''a better sokoban heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    # get all boxes' cordinates to check deadlocks
    box_cor = state.boxes.keys()
    for box in box_cor:
        if (dead_corner_checker(state, box)):
            return math.inf

    return heur_manhattan_distance(state)

    
        
def dead_corner_checker(state, cord):
    # bools for surrounding obstacle
    up = False
    down = False
    left = False
    right = False
    
    # surrouding cordinates
    up_dir = (cord[:1] + ((cord[1] - 1),))
    down_dir = (cord[:1] + ((cord[1] + 1),))
    left_dir = (((cord[0] - 1),) + cord[1:])
    right_dir = (((cord[0] + 1),) + cord[1:])
    dia_dir = (((cord[0] + 1),) + ((cord[1] + 1),))
    
    # surrounding box condition bools
    left_has_box = (left_dir in state.boxes)
    right_has_box = (right_dir in state.boxes)
    up_has_box = (up_dir in state.boxes)
    down_has_box = (down_dir in state.boxes)
    dia_has_box = (dia_dir in state.boxes)
    
    # check surrounding obstacles
    if(cord[1] == 0):
        up = True
    elif (up_dir in state.obstacles):
        up = True
    if (cord[1] == (state.height - 1)):
        down = True
    elif (down_dir in state.obstacles):
        down = True
    if(cord[0] == 0):
        left = True
    elif (left_dir in state.obstacles):
        left = True
    if (cord[0] == (state.width - 1)):
        right = True
    elif (right_dir in state.obstacles):
        right = True
    
    # if deadlock happened
    if ((cord not in state.storage) and 
            (((up or down) and (left_has_box or right_has_box or left or right)) or ((left or right) and (up_has_box or down_has_box)) or
            (down_has_box and right_has_box and dia_has_box))):  
        return True
    else:
        return False
    
    
def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight * sN.hval

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    
    #start timing and initializing SearchEngine
    start = os.times()[0]
    se = SearchEngine('best_first','full')
    se.init_search(initial_state, sokoban_goal_state, heur_fn)
    custom_tb = timebound
    
    #first time search
    goal_state = se.search(custom_tb)
    if(type(goal_state) == bool):
            return False
    result = goal_state
    #cost = (goal_state.gval, math.inf, math.inf)
    #custom_tb -= (os.times()[0] - start)
    
    #loop until false or timebound expires
    while(goal_state): # type(goal_state) != bool
        cost = (goal_state.gval, math.inf, math.inf)
        result = goal_state
        custom_tb = timebound - (os.times()[0] - start)
        goal_state = se.search(custom_tb, cost)
    return result

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    
    #start timing and initializing SearchEngine
    start = os.times()[0]
    se = SearchEngine('custom','full') #astar
    
    #provided wrapped fval function and put it in Engine
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    se.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)
    custom_tb = timebound
    
    #first time search
    goal_state = se.search(custom_tb)
    if(type(goal_state) == bool):
            return False
    result = goal_state
    #cost = (math.inf , math.inf, heur_fn(goal_state) + goal_state.gval)
    #custom_tb -= (os.times()[0] - start)
    
    #loop until false or timebound expires
    while(goal_state): # type(goal_state) != bool
        cost = (math.inf , math.inf, heur_fn(goal_state) + goal_state.gval)
        result = goal_state
        custom_tb = timebound - (os.times()[0] - start)
        goal_state = se.search(custom_tb, cost)
    return result

if __name__ == "__main__":
  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")
  print("Running A-star")

  for i in range(0, 10): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    se.init_search(s0, goal_fn=sokoban_goal_state, heur_fn=heur_displaced)
    final = se.search(timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")

  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit
  print("Running Anytime Weighted A-star")

  for i in range(0, 10):
    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    weight = 10
    final = anytime_weighted_astar(s0, heur_fn=heur_displaced, weight=weight, timebound=timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")