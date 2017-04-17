#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    
#IMPLEMENT
    #init csp
    csp = CSP("tenner_csp_model_1")
    cons = []
    rows_count = len(initial_tenner_board[0])
    #sum row
    sum_row = initial_tenner_board[1]
    
    #init 2d matrix
    board_var = init_var(rows_count, initial_tenner_board)
    
    #all adjcent direction
    adjcent = [(-1,-1), (1,-1),(1,0)]
    
    #cons list for binary row diff
    for qi in range(rows_count):
        for qj in range(9):
            for index in range(qj+1, 10):
                cur_var = board_var[qi][qj]
                cur_comp = board_var[qi][index]
                con = Constraint("C(N{}N{},N{}N{})".format(qi,qj,qi,index),[cur_var, cur_comp]) 
                sat_tuples = []
                for t in itertools.product(cur_var.cur_domain(), cur_comp.cur_domain()):
                    if binary_comp(t):
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
    
    #check adjcent direction
    for qi in range(rows_count):
        for qj in range(10):
            #check remaining direction (adjcent)
            cur_var = board_var[qi][qj]
            for adj in adjcent:
                x_pos = qi + adj[0]
                y_pos = qj + adj[1]
                if ((0<= x_pos < rows_count) and (0 <= y_pos <= 9)):
                    cur_comp = board_var[x_pos][y_pos]
                    con = Constraint("C(N{}N{},N{}N{})".format(qi, qj, x_pos, y_pos),[cur_var, cur_comp]) 
                    sat_tuples = []
                    for t in itertools.product(cur_var.cur_domain(), cur_comp.cur_domain()):
                        if binary_comp(t):
                            sat_tuples.append(t)
                    con.add_satisfying_tuples(sat_tuples)
                    cons.append(con)
                
    
    #cons list for col sum
    col = []
    for col_i in range(10):
        cur_col = [board_var[i][col_i] for i in range(len(board_var))]
        col.append(cur_col)
        
    for i in range(len(col)):
        #corresponding sum
        cur_sum = sum_row[i]
        check_col_sum(col[i], i, cur_sum, cons)
    
    #add all var to csp
    for i in range(rows_count):
        for j in range(10):
            csp.add_var(board_var[i][j])
    
    for c in cons:
        csp.add_constraint(c)
    return csp, board_var

        
def init_var(n, initial_tenner_board):
    dom = [0,1,2,3,4,5,6,7,8,9]
    
    #from stackoverflow
    Matrix = [[-1 for x in range(10)] for y in range(n)]
    
    for i in range(n):
        for j in range(10):
            cur_num = initial_tenner_board[0][i][j]
            if (cur_num == -1):
                num_var = (Variable('N{}N{}'.format(i, j), dom))
                Matrix[i][j] = num_var
            else:
                num_var = (Variable('N{}N{}'.format(i, j), [cur_num]))
                Matrix[i][j] = num_var
    return Matrix

def binary_comp(t):
    return (t[0] != t[1])

def check_col_sum(cur_col, i, cur_sum, cons):
    con = Constraint("Col{}".format(i), cur_col)
    sat_tuples = []
    all_dom = []
    #generate a list for col var
    for var in cur_col:
        all_dom.append(var.cur_domain())
    for t in itertools.product(*all_dom):
        if (sum(t) == cur_sum):
            sat_tuples.append(t)
    con.add_satisfying_tuples(sat_tuples)
    cons.append(con)


##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 8.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary 
       all-different constraints: all-different constraints for the variables in
       each row, contiguous cells (including diagonally contiguous cells), and 
       sum constraints for each column. Each of these constraints is over more 
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''

#IMPLEMENT
    #init csp
    csp = CSP("tenner_csp_model_2")
    cons = []
    rows_count = len(initial_tenner_board[0])
    
    #sum row
    sum_row = initial_tenner_board[1]
    
    #init 2d matrix
    board_var = init_var(rows_count, initial_tenner_board)
    
    #all adjcent direction
    adjcent = [(-1,-1), (1,0), (1,-1)]

    for qi in range(rows_count):
        for qj in range(10):
            #check remaining direction (adjcent)
            cur_var = board_var[qi][qj]
            for adj in adjcent:
                x_pos = qi + adj[0]
                y_pos = qj + adj[1]
                if ((0<= x_pos < rows_count) and (0 <= y_pos <= 9)):
                    cur_comp = board_var[x_pos][y_pos]
                    con = Constraint("C(N{}N{},N{}N{})".format(qi, qj, x_pos, y_pos),[cur_var, cur_comp]) 
                    sat_tuples = []
                    for t in itertools.product(cur_var.cur_domain(), cur_comp.cur_domain()):
                        if binary_comp(t):
                            sat_tuples.append(t)
                    con.add_satisfying_tuples(sat_tuples)
                    cons.append(con)
            
    #form cons that in a row formation(all_diff)
    for i in range(rows_count):
        row_lst = []
        for j in range(10):
            row_lst.append(board_var[i][j])
        row_c = Constraint("C(row{})".format(i), row_lst)
        row_sat_tuples = []
        row_dom = []
        for var in row_lst:
            row_dom.append(var.cur_domain())
        for t in itertools.product(*row_dom):
            if(sum(t) == 45):
                repeat = False
                for num in range(10):
                    if (t.count(num) != 1):
                        repeat = True
                if not repeat:
                    row_sat_tuples.append(t)
        row_c.add_satisfying_tuples(row_sat_tuples)
        cons.append(row_c)
    ##########################################
        
    #cons list for col sum
    col = []
    for col_i in range(10):
        cur_col = [board_var[i][col_i] for i in range(len(board_var))]
        col.append(cur_col)
        
    for i in range(len(col)):
        cur_sum = sum_row[i]
        check_col_sum(col[i], i, cur_sum, cons)
    
    #add all var to csp
    for i in range(rows_count):
        for j in range(10):
            csp.add_var(board_var[i][j])

    for c in cons:
        csp.add_constraint(c)
    return csp, board_var