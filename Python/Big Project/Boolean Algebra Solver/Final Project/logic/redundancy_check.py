try:
    from .identify_variables import *
except ImportError:
    from identify_variables import *

def redundancy_check(problem,print_check = False):
    """
    Find redundancy of terms by looking at factorised terms, to determine term that is to be reduced.

    Args:
        problem (str): problem that was factorised
        print_check (bool): boolean to be used for debugging

    Returns:
        bool: True or False

    Example:
        redundancy_check('A(!B + C) + !CB') returns True
    """
    green = '\033[38;5;34m'
    end = '\033[0m'
    #Cosmetic-------------------------------------------------------------------------------------------------------------
    common_var = re.findall(r'([A-Za-z0-9_!]+)\s*\(', problem)[0]  # finds the characters in front of '('
    problem_inside_bracket = extract_problem_in_brackets(problem)

    if (factorised_term := common_var + '(' + problem_inside_bracket + ')') == problem: #if factorised term is the problem, no redundancy as redundancy requires 2+ terms
        return False

    problem_without_factorised_term = problem.replace(' + ' + factorised_term,'')
    problem_without_factorised_term = problem.replace(factorised_term + ' + ','') #remove factorised term
    unfactorised_terms = problem_without_factorised_term.split(' + ')
    factorised_terms = problem_inside_bracket.split(' + ') #find individual terms inside bracket
    complement_of_factorised_terms = []
    for term in factorised_terms:
        if len(term) == 1 or len(term) == 2 and term[0] == '!':
            #check if it's single variable
            if term[0] == '!':
                complement_of_factorised_terms.append(term[1:])
            else:
                complement_of_factorised_terms.append('!' + term)
    #find complements of terms in bracket

    for term in unfactorised_terms:
        not_var, var = identify_variables(term)
        if all(each_var in complement_of_factorised_terms for each_var in not_var) and all(each_var in complement_of_factorised_terms for each_var in var): #if complement of each terms exists
            #problem = ' + '.join(unfactorised_terms) + ' + ' + common_var
            if print_check:
                print(f'\n{green}REDUNDANCY DETECTED: {term} COVERS FOR {common_var}, WHEN TERMS INSIDE BRACKET ARE 0{end}')
            return True

    return False

if __name__ == '__main__':
    #problem = '!B!C + !B!D + !B!E + !C!D + !C!E + !D!E + A(B + C + D + E)'
    problem = 'A(!B + C) + !CB'
    print(redundancy_check(problem))