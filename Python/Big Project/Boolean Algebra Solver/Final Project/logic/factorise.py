try:
    from .redundancy_check import *
except ImportError:
    from redundancy_check import *

import re

def find_most_common_factor(terms,checks):
    """
    Find most common factor among the terms

    Args:
        terms (list): terms in the problem
        checks (list): list to prevent used common factors to be used again

    Returns:
        tuples: (most common factor(str), common terms(str))

    Example:
        find_most_common_factor(['AE', 'AC', 'BD'],[]) returns ('A', ['AE', 'AC'])
    """
    all_var = []
    for term in terms:
        not_var, var = identify_variables(term) #identify variables in each terms
        for each_var in var:
            all_var.append(each_var)
        for each_not_var in not_var:
            all_var.append(each_not_var)

    for check in checks: #remove used common factors.
        all_var = [var for var in all_var if var != check]

    freq_var = {} #dictionary of variables, to store number of terms that has that variable.
    for var in all_var:
        if var not in freq_var:
            freq_var[var] = freq_var.get(var, 1)
        else:
            freq_var[var] = freq_var[var] + 1

    if not freq_var: #Not factorisable.
        return '', ''

    highest_factor = max(freq_var.values()) #find highest number of terms that a variable is inside the terms.
    possible_most_common_var = [k for k, v in freq_var.items() if v == highest_factor] #most common variables.
    most_common_var = []

    temp_freq = {} #dictionary to store key of variable, to values of term containing that variable.
    for each_var in possible_most_common_var:
        for term in terms:
            not_var, var = identify_variables(term)
            if each_var not in temp_freq: #create dictionary of each_var
                temp_freq[each_var] = []
            if each_var in not_var or each_var in var: #checks whether the term has most common variable, and append.
                temp_freq[each_var].append(term)

    if len(temp_freq) == 1: #Only 1 most frequent common factor
        most_common_var = ''.join(list(temp_freq.keys()))
        common_terms = list(temp_freq.values())[0]
        return most_common_var, common_terms

    for i in range(len(possible_most_common_var)):
        for j in range(i + 1, len(possible_most_common_var)):
            key1 = possible_most_common_var[i]
            key2 = possible_most_common_var[j]
            if temp_freq[key1] == temp_freq[key2]:
                most_common_var.append(key1)
                most_common_var.append(key2)

    if most_common_var:
        most_common_var = ''.join(most_common_var)
    else:
        most_common_var = max(freq_var, key=freq_var.get)
        common_terms = temp_freq[most_common_var]
        return most_common_var, common_terms

    common_terms = []
    for term in terms:
        #not_var, var = identify_variables(term)
        if most_common_var in term:
            common_terms.append(term)

    if common_terms:
        return most_common_var, common_terms
    return '',''

def factorise(problem,check):
    """
    Factorise the terms by first finding whether every term has a common factor, then proceed to finding the most common factor among the terms, then factorise the terms.

    Args:
        problem (str): problem
        check (list of str): list to prevent used common factors to be used again

    Returns:
        string: factorised problem.

    Example:
        factorise('AE + AC + BD',[]) returns 'BD + A(E + C)'
    """
    terms = problem.split(' + ')
    temp_terms = terms.copy()
    common_var = find_common_variables(temp_terms)
    common_var = ''.join([var for var in common_var if var not in check]) #remove checked factors

    if len(terms) == 1: #only 1 term
        return problem

    if not common_var: #No common variables with all the terms
        common_var, factored_terms = find_most_common_factor(temp_terms,check)
        if not common_var:
            return problem
        if len(factored_terms) < 2: #means it is not factorisable.
            return problem
    elif common_var:
        factored_terms = terms.copy()

    not_var, var = identify_variables(common_var)
    factorisable_terms = factored_terms
    unfactored_terms = [term for term in temp_terms if term not in factorisable_terms]

    for i,term in enumerate(factored_terms): #getting terms inside bracket after factorising
        for each_not_var in not_var:
            factored_terms[i] = factored_terms[i].replace(each_not_var, '')
        for each_var in var:
            factored_terms[i] = factored_terms[i].replace(each_var, '')

    if unfactored_terms: #Unfactorised term exists
        factorised_form = ' + '.join(unfactored_terms) + ' + ' + common_var + '(' + ' + '.join(factored_terms) + ')'
    else:
        factorised_form = common_var + '(' + ' + '.join(factored_terms) + ')'
    #print(f'\n{factorised_form} ||    factorise by {common_var} from {problem}:')
    return factorised_form

def simplify_and_merge_factorised_form(factorised_form, insert = '',print_check = False):
    """
    Replaces term in bracket with simplified terms, then merge them together.
    Only applicable when factorised form is true

    Args:
        factorised_form (str): factorised problem.
        insert (str): the problem inside bracket that was simplified.
        print_check (bool): boolean used for printing out steps & debugging.

    Returns:
        string: merged problem.

    Example:
        simplify_and_merge_factorised_form('!AB + A(!B + BC)', '!B + C') returns '!AB + !BA + AC'
    """
    green = '\033[38;5;34m'
    blue = "\033[34m"
    red = '\033[91m'
    end = '\033[0m'
    #Cosmetic------------------------------------------------------------------------------------------

    common_var = re.findall(r'([A-Za-z0-9_!]+)\s*\(', factorised_form)[0] #finds the characters in front of '('
    problem_inside_bracket = extract_problem_in_brackets(factorised_form)

    factorised_term = common_var + '(' + problem_inside_bracket + ')'

    if insert == '1': #terms in bracket simplifies to 1
        simplified_factorised_form = factorised_form.replace(problem_inside_bracket, '1')
        if print_check:
            display_factorised_form = factorised_form.replace(common_var + '(' + problem_inside_bracket + ')',f'{red}{common_var}({problem_inside_bracket}){end}')
            factorised_form = factorised_form.replace(factorised_term,common_var)

            display_simplified_factorised_form = simplified_factorised_form.replace(common_var + '(1)',f'{red}{common_var}(1){end}')
            print(f'{green}REPLACE TERMS IN BRACKET WITH SIMPLIFIED TERMS{end}')
            print(f'{display_factorised_form} = {display_simplified_factorised_form}')
            print(f'= {display_simplified_factorised_form.replace('(1)','')}')
        else:
            factorised_form = factorised_form.replace(factorised_term, common_var)

        return factorised_form

    terms_inside_bracket = insert.split(' + ')
    merged_terms = terms_inside_bracket.copy()
    for i,term in enumerate(terms_inside_bracket):
        merged_terms[i] = terms_inside_bracket[i] + common_var #merge them together.

    merged_terms = ' + '.join(merged_terms)
    merged_terms = sort_problem(merged_terms)
    merged_terms = ' + '.join(merged_terms)
    merged_form = factorised_form.replace(factorised_term,merged_terms)

    simplified_factor_form = factorised_form.replace(problem_inside_bracket, insert) #returns simplified problem.

    #Cosmetic-----------------------------------------------------------------------------------------------------------
    if print_check:
        display_factorised_form = factorised_form.replace(common_var + '(' + problem_inside_bracket + ')', f'{red}{common_var}({problem_inside_bracket}){end}')
        display_simplified_factor_form = simplified_factor_form.replace(common_var + '(' + insert + ')', f'{red}{common_var}({insert}){end}')
        display_merged_form = merged_form.replace(merged_terms,f"{red}{merged_terms}{end}")

        print(f'\n{green}REPLACE TERMS IN BRACKET WITH SIMPLIFIED TERMS{end}')
        print(f'{display_factorised_form} = {display_simplified_factor_form}')
        print(f'= {display_merged_form}')

    return merged_form

if __name__ == '__main__':
    #!X + XBC + XFG = #!X + X(BC + FG)
    #problem = 'XBC + XFG + !X + A + XBCFG'
    #problem = '!AB + !A!B + B!A + BA'
    problem = '!A'
    #terms = sort_problem(problem)

    #problem = 'AB + AC'
    #problem = 'A(B + C)'
    problem = 'AE + AC + BD'
    terms = sort_problem(problem)
    #problem = 'A + B'
    print(terms)
    print(factorise(problem,[]))
    print(extract_problem_in_brackets(factorise(problem,[])))
    #print(find_most_common_factor(terms,[]))
    #print(simplify_and_merge_factorised_form(problem, 'B + C + D'))
    #print(find_common_variables(problem))
    #print(find_most_common_factor(terms,['A','B']))
    #print(factorise(problem, find_most_common_factor(problem,[])))
    #print(find_most_common_factor(terms,[]))
    #print(simplify_and_merge_factorised_form('!AB + A(!B + BC)', '!B + C'))
    #print(factorise(problem,[]))