import re

def substitute_with_number(expression, combination, list_of_variables=None):
    """
    verify whether a single Boolean equation is true for a given combination of variables
    by substitute the equation with '1' and '0' based on combination.

    Args:
        expression (str): the expression to be substituted with number
        combination (list): list of variables that are '1', meaning true

    Returns:
        string: '1' or '0', depending on validity of the expression after substitution

    Example:
        substitute_with_number('ABC + BC', ['A','B']) returns '0'.
        substitute_with_number('ABC + BC', ['A','B', 'C']) returns '1'.
    """
    for var in combination:
        if var != '':
            expression = expression.replace('!'+var,'0') #replace Not variables with 0
            expression = expression.replace(var, '1')

    expression = re.sub('![A-Za-z]','1', expression) #replace !
    expression = re.sub('[A-Za-z]', '0', expression) #replace 0
    expression = ['1' if term.replace('1', '') == '' else '0' for term in expression.split(' + ')]
    #check whether any of the terms = '1'

    if '1' in expression:
        return '1'
    else:
        return '0'

def verify_solution(problem,solution):
    """
    Verify whether problem and solution are equivalent
    by looping through all possible combinations of variables.

    Prints out truth table along the way

    Algorithm:
        Identifies each distinct variables in the problem
        Create a list of combinations based on the variables identified, example: ABCD, the combination would be (0000 --> 1111)
        verify equivalence between problem and solution for each combination
        print the truth table

    Args:
        problem (str): the original problem
        solution (list): the simplified solution

    Returns:
        bool: true if equivalent, false if not equivalent

    Example:
        verify_solution('ABC + B', 'B') returns true
        verify_solution('ABC + B', 'E') returns false
    """
    list_of_combinations = []
    check = True

    list_of_variables = sorted(set(re.findall('[a-zA-Z]', problem))) #find all the variables
    n = len(list_of_variables)

    for mask in range(1 << n):  # obtain total no. of combination in binary ( 000 --> 111)
        combination = []
        for i in range(n):  # Loop via index of the list
            bit_mask = (1 << i)  # make a bit_mask that represents the variable, to be masked example: (A = 001, B = 010, C = 100)

            if mask & bit_mask:  # if the variable is in the mask, append it to combination
                combination.append(list_of_variables[i])
        list_of_combinations.append(combination)

    print('\n=== Truth table ===')
    print(f'{(" ").join(list_of_variables)[::-1]} | P | S')
    print(f'{'-' * (2 * n + 7)}')

    for combination in list_of_combinations: #loop against combinations
        problem_with_values = substitute_with_number(problem, combination)
        solution_with_values = substitute_with_number(solution, combination, ''.join(list_of_variables))
        display_truth_table(combination,list_of_variables,problem_with_values,solution_with_values)
        if problem_with_values != solution_with_values:
            check = False

    return check

def display_truth_table(combination,list_of_variables,problem,solution):
    """
    Prints one line of the truth table through the passed parameters

    Args:
        combination (list): list of variables that are '1', meaning true
        list_of_variables (list): list of all the distinct variables
        problem (str): original problem that was substituted with '1' or '0'
        solution (str): simplified solution that was substituted with '1' or '0'
    """

    if list_of_variables is not None:
        list_of_variables = ''.join(list_of_variables)
        for var in combination:
            list_of_variables = list_of_variables.replace(var, '1')
        list_of_variables = re.sub('[A-za-z]','0', list_of_variables)
        print(f'{" ".join(list_of_variables)[::-1]} | {problem} | {solution}')

def handle_input_error(problem):
    """
    Checks whether the problem is input in a valid format

    Args:
        problem (str): The input made by user

    Note:
        the format has to be terms separated by ' + '.
        Example is 'ABC + B!C + C'
    """
    input_error = False
    if (re.search('[^A-Za-z0-9+ !]',problem)): #Other characters in problem
        input_error = True
    elif (re.search(r'!{2,}',problem)):#consecutive NOT '!'
        input_error = True
    elif (re.search(r'\+{2,}',problem)): #consecutive plus signs (++)
        input_error = True
    elif (re.search(r'\+(?!\s*[A-Za-z!])',problem)): #After '+' must be optional spaces then a variable or '!'
        input_error = True
    elif (re.search(r'![\s\+\!]',problem)):
        input_error = True

    return input_error

if __name__ == '__main__':
    print(substitute_with_number('ABC + BC', ['A','B', 'C']))


