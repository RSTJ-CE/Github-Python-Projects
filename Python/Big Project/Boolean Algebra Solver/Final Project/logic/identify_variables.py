import re

def sort_term(term):
    """
    Sort term, starting with not_variables, alphabetically & filter out to get unique variables in the process
    Purpose is to make it easier to visualise & easier for other helper functions to simplify the term

    Args:
        term (str): term

    Returns:
        string: arranged term

    Example:
        sort_term(AAB!CD!E) returns '!C!EABC'.
    """
    not_var,var = identify_variables(term)
    term = ''.join(not_var + var)

    return term

def sort_problem(problem):
    """
        Split up the problem into terms for helper functions to set & sort them alphabetically.
        Purpose: to carry out AND simplifications easily.

        Args:
            problem (str): problem to be simplified

        Returns:
            terms: terms inside the problem

        Example:
            sort_problem('AB!C + DCE + !A!B') returns ['!CAB','CDE','!A!B'].
        """
    terms = identify_terms(problem)
    for i,term in enumerate(terms):
        terms[i] = sort_term(term)

    return terms

def identify_variables(term):
    """
    Identify variables inside a term, set & sort them accordingly as tuples.
    Purpose: to make it easier for other helper functions when simplifying terms

    Args:
        term (str): term

    Returns:
        tuple: (list of not_variables, list of variables) inside the term

    Example:
        identify_variables('AB!CD!E') returns (['!C','!E'],['A','B','D']).
    """

    not_filter = r'![A-Za-z0-9]'
    not_var = sorted(set(re.findall(not_filter, term))) #re.findall finds not_variables in string
    var = sorted(set(re.sub(not_filter, '', term))) #re.sub replaces not_variables in string
    return not_var, var

def identify_terms(problem):
    """
    Split problem into terms

    Args:
        problem (str): problem to be simplified

    Returns:
        list: list of terms inside the problem

    Example:
        identify_terms('AB + !CD + ABCD') returns ['AB','!CD','ABCD'].
    """
    problem = problem.split(' + ')
    return problem

def find_common_variables(terms):
    """
    Find common variables across terms
    Purpose is to find common variables to carry out factorisation, simplifications.

    Args:
        terms (list): terms that we want to find common variables

    Returns:
        common_var (list): common variables

    Example:
        find_common_variables(['ABCD','CDE']) returns 'CD'.
    """
    common_var = None
    for term in terms:
        not_var, var = identify_variables(term) #identify variables in each term
        current = set(not_var) | set(var) #create a set of variables for each term
        common_var = current if common_var is None else common_var & current #keep variables shared across terms
    common_var = sort_term(''.join(list(common_var))) #convert to string & sort them
    return common_var

def find_complements(terms):
    """
    Find complements across the terms, such as !A and A.
    Purpose is to find complements to carry out simplifications.

    Args:
        terms (list): terms that we want to find complements

    Returns:
        complements (list): complements of the terms.

    Example:
        find_complements(['ABCD','!CD!E']) returns 'C'. because 'C' is in first term, '!C' in second term.
    """
    not_var_store = []
    var_store = []
    #list to store variables.
    for i,term in enumerate(terms):
        terms[i] = sort_term(term) #sort each terms, and replace them into the list.
        not_var, var = identify_variables(term) #identify variables
        not_var = ''.join(not_var).replace('!','') #removes '!' from not variables to compare with variables.
        not_var = [each_not_var for each_not_var in not_var] #turns into a list
        for each_not_var in not_var:
            not_var_store.append(each_not_var)
        for each_var in var:
            var_store.append(each_var)
        #Store each variable into list.

    complements_store = [var for var in var_store if var in not_var_store] #finds common variable between not_var_store & var_store. they are complements.
    complements = []
    for complement in complements_store: #remove duplicates
        if complement not in complements:
            complements.append(complement)

    return complements

def extract_problem_in_brackets(factorised_form):
    """
    Extracts the terms inside brackets, for example: AB(C + D), it extracts 'C + D' to be used for simplification in other functions

    Args:
        factorised_form (str): term that was factorised.

    Returns:
        string: extracted problem in the brackets

    Example:
        extract_problem_in_brackets('BD + A(E + C)') returns 'E + C'
    """
    inside_bracket = re.findall(r'\((.*?)\)', factorised_form) #find terms covered by brackets, as a list.
    terms_inside_bracket = inside_bracket[0].split(' + ') #split by ' + ' sign.
    problem_inside_bracket = ' + '.join(terms_inside_bracket) #join them together as a string
    return problem_inside_bracket

if __name__ == '__main__':
    term = '!AAAB!VASDACSE!D'
    problem = '!AAAB!VASDACSE!D + ABCDE'
    print(f'identified variables = {identify_variables(term)}')
    #Not on the left, compliment on the right
    print(f'sorted term = {sort_term(term)}')
    print(f'sorted problem = {identify_terms(problem)}')

    terms_2 = identify_terms('AB + ABC')
    print(f'common variable = {find_common_variables(terms_2)}' + '\n')

    #terms_3 = sort_problem('Y!X!Z + X')
    terms_3 = sort_problem('!X + XBC + XFG')
    #Y(X!Z + !X)
    #Y(X!ZB + !XA

    #Y!X!Z + XY = Y(!X!Z + X) = Y(X + !Z) = YX + Y!Z
    print(f'sorted {terms_3}')
    print(f'complements = {find_complements(terms_3)}')


