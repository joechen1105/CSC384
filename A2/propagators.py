#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newVar=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newVar (newly instaniated variable) is an optional argument.
      if newVar is not None:
          then newVar is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newVar = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newVar = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
#IMPLEMENT
    pruned_var = []
    cons = []
    if not newVar:
        cons = csp.get_all_cons()
    else:
        cons = csp.get_cons_with_var(newVar)
    
    for c in cons:
            if (len(c.get_unasgn_vars()) == 1):
                if (FC(c, c.get_unasgn_vars()[0], pruned_var)):
                    return False, pruned_var

    #all constraints have been checked
    return True, pruned_var
    

def FC(c, var, pruned_var):
    #for each member of CurDom
    for d in var.cur_domain():
        #if d falsifies c, prune it
        if not (c.has_support(var, d)):
            var.prune_value(d)
            pruned_var.append((var, d))
        #DWO checking
        if (var.cur_domain_size() == 0):
            return True
    return False


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    
    GAC_q = []
    pruned_var = []
    
    if not newVar:
        for c in csp.get_all_cons():
            GAC_q.append(c)
    else:
        for c in csp.get_cons_with_var(newVar):
            GAC_q.append(c)

    if GAC_Enforce(csp, GAC_q, pruned_var):
        return True, pruned_var
    else:
        return False, pruned_var
    

def GAC_Enforce(csp, GAC_q, pruned_var):
    while (len(GAC_q) != 0):
        c = GAC_q.pop(0)
        for v in c.get_unasgn_vars():
            for d in v.cur_domain():
                if not (c.has_support(v, d)):
                    v.prune_value(d)
                    pruned_var.append((v, d))
                    #DWO
                    if (v.cur_domain_size() == 0):
                        del GAC_q[:]
                        return False
                    else:
                        for c_with_var in csp.get_cons_with_var(v):
                            GAC_q.append(c_with_var)
    return True



















