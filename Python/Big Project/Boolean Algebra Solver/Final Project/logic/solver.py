try: #for running as a package
    from .factorise import *
    from .redundancy_check import *
    from .or_simplification import *
    from .Error_handling import verify_solution
except ImportError: # for running directly
    from factorise import *
    from redundancy_check import *
    from or_simplification import *
    from Error_handling import verify_solution

def solver(problem,print_check = False,checked_common_variables = None, factorise_history = None,already_factorised_form = None):
    """
    Simplifies boolean algebra expressions logic recursive simplification with OR theorems and factorisations

    Algorithm:
        Simplify with OR: simplifies the problem with OR theorems logic helper function: or_simplification()
        Factorise: factorises the problem logic helper function: factorise()
        Simplify problem inside brackets: Extracts problem inside brackets from factorised form logic helper function: extract_problem_in_brackets(), and simplifies it by calling itself: solver()
        Merging factorised form: After problem in brackets is simplified, factorised form merges logic helper function: simplify_and_merge_factorised_form()
        Recursion: The merged factorised form gets put into solver() until it can no longer be simplified

    Args:
        problem (str): boolean algebra expression that is to be simplified
        print_check (bool): Enable to True to show workings/used for debugging to track states
        checked_common_variables (list): stores common variables that has already been used for factorisation attempts, to prevent infinite recursion
        factorise_history (list): stores factorisation history of the expression for printing and debugging during recursion
        already_factorised_form (list): stores factorised forms that has already been attempted to be simplified, to prevent infinite recursion

    Returns:
        str: Simplified boolean expression

    Examples:
        solver('AB + A + BC') returns 'A + BC'
        solver('ABC + !ABC + AB + !AB') returns 'B'

    Notes:
        function unable to handle terms with brackets
        function requires specific format of terms separated by ' + '
        color-coded output when print_check == True for better visualization
        Dependent on helper functions: sort_problem(),or_simplification(),factorise(),extract_problem_in_brackets(),find_most_common_variable(),redundancy_check(),identify_variables(),simplify_and_merge_factorised_form()
    """

    blue = "\033[34m"
    green = '\033[38;5;34m'
    end = '\033[0m'
    #Cosmetic for showcase of working----------------------------------------------------------

    #Initialize storage parameters if not provided
    if checked_common_variables is None:
        checked_common_variables = []
    if factorise_history is None:
        factorise_history = []
    if already_factorised_form is None:
        already_factorised_form = []

    temp_check = checked_common_variables.copy() #copy of checked_common_variables at beginning of function to be compared to checked_common_variables at the end, to decide whether to return problem or continue recursion
    problem = ' + '.join(sort_problem(problem))
    or_problem = or_simplification(problem) #use OR theorems to simplify
    factorised = factorise(or_problem,checked_common_variables) #Attempt to factorise

    if factorise_history and print_check == True:
        #printing for debugging and showcase working, if there are factorised forms.
        print(f'\n{blue}ATTEMPT TO FACTORISE{end}')
        if problem != or_problem:
            #if problem can be simplified, show factorising history and show simplification steps
            if len(factorise_history) > 1:
                print(f'{problem} <--- {factorise_history[-1]} <--- {factorise_history[-2]}')
                print(f'\n{green}SIMPLIFY WITH OR, AND THEOREMS{end}')
                or_simplification(problem, print_check)

            else:
                print(f'{problem} <--- {factorise_history[-1]}')
                print(f'\n{green}SIMPLIFY WITH OR, AND THEOREMS{end}')
                or_simplification(problem, print_check)

        else:
            #if problem cannot be simplified, show factorising history of up to 2.
            if len(factorise_history) > 1:
                print(f'{problem} <--- {factorise_history[-1]} <--- {factorise_history[-2]}')
            else:
                print(f'{problem} <--- {factorise_history[-1]}')
    elif problem != or_problem and not factorise_history and print_check == True:
        #no factorised form and can be simplified,
        print(f'\n{green}SIMPLIFY WITH OR, AND THEOREMS{end}')
        or_simplification(problem,print_check)


    if factorised != or_problem:
        #if able to factorise
        if not factorised in already_factorised_form:
            #stores factorised form to prevent factorising it again later, leading to redundant steps
            already_factorised_form.append(factorised)
            factorise_history.append(factorised)
        prob = extract_problem_in_brackets(factorised) #Extract problem in bracket from factorised form
        simplified_prob = solver(prob,print_check,[],factorise_history,already_factorised_form) #simplify problem in bracket

        if simplified_prob == prob:
            #problem in bracket cannot be simplified with OR theorems
            if redundancy_check(factorised,print_check):
                #attempt redundancy check
                simplified_problem = simplify_and_merge_factorised_form(factorised,'1',print_check)
            else:
                #no redundancy, find most common factor of the problem and append it to checked_common_variables, to prevent factorising it again later, leading to redundant steps
                simplified_problem = or_problem.split(' + ')
                common_var,similar_term = find_most_common_factor(simplified_problem,checked_common_variables)
                not_var, var = identify_variables(common_var)
                for each_not_var in not_var:
                    checked_common_variables.append(each_not_var)
                for each_var in var:
                    checked_common_variables.append(each_var)
                simplified_problem = ' + '.join(simplified_problem)

        else:
            #problem in brackets can be simplified, merge the simplified form
            simplified_problem = simplify_and_merge_factorised_form(factorised,simplified_prob,print_check)

    else:
        #cannot factorise
        simplified_problem = or_problem

    if simplified_problem == problem and temp_check == checked_common_variables:
        #cannot be simplified further
        return simplified_problem
    else:
        #attempt recursive simplification, to prevent missing possible simplifications
        return solver(simplified_problem,print_check, checked_common_variables,[],already_factorised_form)

def recursive_factorisation(problem, factorised_terms = None):
    """
    Factorises boolean expressions recursively starting with most common factors, until no factorisation is possible.

    Algorithm:
        factorisation: It factorises the problem logic factorise() helper function
        detects factorised term: It finds the factorised terms logic re module, then removes it from the problem and appends it to factorised_terms(list)
        recursion: The new problem gets sent back into the function, and repeats until no factorisation is possible

    Args:
        problem (str): problem that is to be factorised.
        factorised_terms (list): stores factorised terms that was factorised in previous recursion

    Returns:
        list: factorised terms that cannot be factorised anymore

    Examples:
        Example: AB + AC + DE + EF returns ['A(B + C)','E(D + F)']
        Example 2: AB + AC + GF + EG + EF + EXY returns ['E(G + F + XY)', 'A(B + C)', 'GF']

    Notes:
        problem is assumed to be pre-validated by previous functions, thus no edge cases
        dependent on helper functions: factorise(), extract_problem_in_brackets()
    """

    if factorised_terms is None:
        factorised_terms = []

    factorised_problem = factorise(problem,[]) #factorises problem
    if factorised_problem == problem:
        #cannot factorise anymore
        if factorised_problem not in factorised_terms:
            #add factorised_problem into list if not in list, to prevent duplicates
            factorised_terms.append(factorised_problem)
        return factorised_terms

    common_var = re.findall(r'([A-Za-z0-9_!]+)\s*\(', factorised_problem)[0] #extract factor from factorised problem
    problem_inside_bracket = extract_problem_in_brackets(factorised_problem) #extract problem in bracket from factorised problem
    factorised_term = common_var + '(' + problem_inside_bracket + ')' #merge to get term that is factorised

    factorised_terms.append(factorised_term) #stores the factorised terms
    factorised_problem = factorised_problem.replace(' + ' + factorised_term,'') #removes factorised terms in original problem

    return recursive_factorisation(factorised_problem,factorised_terms)

def xnor_xor_check(problem):
    """
    Detects for 2-variable xnor/xor in problem and replaces them with their xnor/xor form

    Algorithm:
        detecting for XOR/XNOR: For every term, it generates opposite term that createst it's XNOR/XOR form and compare whether it is in the problem.
        merging into xnor/xor form: Once detected, it stores the characters and replaces their original form with 'XOR' or 'XNOR' depending on whether their condition passes

    Args:
        problem (str): problem to be simplified

    Returns:
        str: simplified problem with xnor/xor form

    Examples:
        Example 1: xnor_xor_check('!BC + !CB + BD + !B!D + A') returns B XOR C + B XNOR D + A
        Example 2: xnor_xor_check('!Y!Z + !X + YZ + W') returns Y XNOR Z + !X + W

    Notes:
        dependent on helper functions: sort_term(),identify_variables()
    """
    terms = problem.split(' + ')
    temp_terms = terms.copy() #to check against original problem before any simplification is made

    for term in terms:
        opp_var = [] #store opposite variable: example 'A' in term , it stores '!A'
        opp_not_var = [] #store opposite variable: example '!A' in term, it stores 'A'
        char_list = [] #store characters that is in XNOR/XOR term. example AB + !A!B --> stores A, B as they are XNOR terms

        not_var,var = identify_variables(term) #identify variables of term
        for each_not_var in not_var:
            opp_var.append(each_not_var.replace('!',''))
        for each_var in var:
            each_var = '!' + each_var
            opp_not_var.append(each_var)
        if len(not_var) + len(var) == 2:
            #detects 2-variable term
            if not opp_var or not opp_not_var:
                #checks whether opposite XNOR term exists in the expression
                xnor_term = ''.join(opp_not_var) + ''.join(opp_var)
                if xnor_term in terms:
                    xnor_string = sort_term(xnor_term.replace('!',''))
                    for char in xnor_string:
                        char_list.append(char)
                    xnor_string = ' XNOR '.join(char_list)
                    if xnor_string not in temp_terms:
                        own_index = temp_terms.index(term)
                        index_of_other_term = temp_terms.index(xnor_term)
                        temp_terms.pop(own_index)
                        temp_terms.insert(own_index, xnor_string)
                        temp_terms.pop(index_of_other_term)
            else:
                #checks whether opposite XOR term exists in the expression
                xor_term = ''.join(opp_not_var) + ''.join(opp_var)
                if xor_term in terms:
                    xor_char = sort_term(xor_term.replace('!',''))
                    for char in xor_char:
                        char_list.append(char)
                    xor_string = ' XOR '.join(char_list)
                    if xor_string not in temp_terms:
                        own_index = temp_terms.index(term)
                        index_of_other_term = temp_terms.index(xor_term)
                        temp_terms.pop(own_index)
                        temp_terms.insert(own_index, xor_string)
                        temp_terms.pop(index_of_other_term)

    problem = ' + '.join(temp_terms)
    return problem

def main(original_problem,print_check=False):
    """
    Main logic that combines all helper functions, includes verification to prevent wrong simplification,
    and factorises the most common factor that cannot be simplified anymore

    Algorithm:
        Sorts the problem into alphabetical order.
        Simplify the problem using solver() helper function.
        Verify the accuracy of the solution using verify_solution() helper function.
        Factorise the final solution based on the most common factor
        Find XNOR and XOR terms and present them.

    Args:
        original_problem (str): original problem to be simplified
        print_check (bool): if true, prints the working for debugging

    Returns:
        tuples: sorted_problem (str), result (str)

    Examples:
        main('ABC + !ABC + AB + !AB', True)
        returns ('ABC + !ABC + AB + !AB', 'B')

        main('XYZ + XYW + XZW + YZW + !XY + !XZ + !YW + X!Y!Z + !X!Y!W',True)
        returns ('XYZ + WXY + WXZ + WYZ + !XY + !XZ + !YW + !Y!ZX + !W!X!Y', 'Y XNOR Z + !X + W')
    Notes:
        Problem must be in format of terms separated by ' + '. (handled by input validation in the GUI)
    """
    sorted_problem = ' + '.join(sort_problem(original_problem))
    simplified = solver(original_problem,print_check)

    if not verify_solution(original_problem,simplified):
        return 'Solution not found','Solution not found'

    factored_terms = recursive_factorisation(simplified)

    factored_form = ' + '.join(factored_terms)

    for i,term in enumerate(factored_terms):
        if term[-1] == ')': #only factorised terms allowed
            problem_inside_brackets = extract_problem_in_brackets(term)
            simplified_with_xor_xnor = xnor_xor_check(problem_inside_brackets)
            new_term = term.replace(problem_inside_brackets,simplified_with_xor_xnor)
            factored_terms.pop(i)
            factored_terms.insert(i, new_term)
        else:
            #not factorised
            simplified_with_xor_xnor = xnor_xor_check(term)
            new_term = term.replace(term,simplified_with_xor_xnor)
            factored_terms.pop(i)
            factored_terms.insert(i, new_term)

    result = ' + '.join(factored_terms)
    return sorted_problem,result
    
if __name__ == "__main__":
    print(main('XYZ + XYW + XZW + YZW + !XY + !XZ + !YW + X!Y!Z + !X!Y!W',True))
    #print(main('ABC + !ABC + AB + !AB', True))

    # original_problem = "!AX + A!C + X!C"
    # original_problem = "AB + AC + AD + AE + AF + AG + BC + BD + BE + BF + BG + CD + CE + CF + CG + DE + DF + DG + EF + EG + FG + !AB + !AC + !AD + !AE + !BC + !BD + !CD + A!E + !AF + B!G + !BG + !C!D + C!D + !CD + A!B + !AB + A!C + !AC + !DE + D!E + !EF + E!F + !GA + G!A"
    # original_problem = 'A!B!C + ABC + A!B!D + ABD + !AB!C + !A!BC + !AB!D + !A!BD + !CD + C!D'
    # original_problem = 'XYZ + XYW + XZW + YZW + !XY + !XZ + !YW + X!Y!Z + !X!Y!W'
    # original_problem = '!A!BY + !AB!Y + !X!Y + XY + X!A + XB + XY
    # original_problem = 'A + BA + !AB + CBA + C!A!B + !CAB'
    # original_problem = 'AB + A + !AC + BC'
