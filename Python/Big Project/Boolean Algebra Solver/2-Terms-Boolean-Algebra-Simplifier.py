#Second project: 2 terms boolean algebra solver with string manipulation python
#RSTJ

#the project works by
#1. scanning and locating index of '!' in the string, then add 1 to the index to locate variables that are 'nots'.
#2. splitting string by ' ', to find the terms in equation
#3. each terms in the variables are split into not_var and var which is used for simplification in other functions
#4. during simplification, each separated terms gets put into 'AND' simplifier, then it gets combined and put into 'OR' simplifier
#5. After simplification, it factorises the terms and then simplify the terms in brackets
#6. Final expression is derived through this method

def check_for_error(problem):
    terms = problem.split('+')
    spacing = problem.count(' ') #counts number of spacing
    plus = problem.count('+') #counts number of +
    problem_check = all(ch.isalpha() or ch.isdigit() or ch == '+' or ch == ' ' or ch == '!' for ch in problem) #Return true if valid characters

    if problem_check == False: #checks if characters are valid
        return 'Invalid input'
    if problem[-1] == '!': #checks for typo
        return '! is not allowed as the last variable'
    if '(' in problem or ')' in problem: #declines brackets
        return 'Brackets are not accepted'
    if len(terms) > 2: #enforces only 2 operands or 1
        return 'Maximum 2 terms'
    if (spacing > 0 and plus == 0) or spacing > 2: #ensure correct spacing
        return 'Please ensure correct spacing'
    elif (plus == 1):
        plus_index = problem.index('+')
        if (problem[plus_index-1] != ' ' or problem[plus_index+1] != ' '):
            return 'Please ensure correct spacing'
    if len(terms) < 2:
        return 'single' #returns single if only 1 term, for simplification
    if not problem.strip(): #declines empty input
        return 'please enter a valid input'
    if '!!' in problem: #checks for typos like !!
        return "Ensure '!' is typed correctly"
    if terms[0] in ('',' ') or terms[-1] in ('', ' '): #check if there are any equation errors, like +a or ++
        return 'Terms are not accepted'


    return 'pass'

def sort_variable(variable): #sorts variable by alphabetical order
    not_index = [] #list used to store indexes of '!'
    dic_var = {} #dictionary to store variables that has '!' in front, and how many of the same variables has '!' infront
    sorted_variable_without_not = ''.join(sorted(variable)).replace('!', '')  #string of arranged problem without '!'
    index = variable.find('!')

    while index != -1: #finds variables that has '!' in front of it, denoting it is a not variable
        not_index.append(index + 1) #variables that has '!' in front of it
        index = variable.find('!', index + 1) #scan for next variable with '!' in front of it
    not_variables = [variable[i] for i in range(len(variable)) if i in not_index]  #return list of the variables that has '!' in front of it

    for not_var in not_variables:  #store not variables as dictionary
        dic_var[not_var] = dic_var.get(not_var,0) + 1  # assigning values to dictionary , where key is variable, value is occurrence amount

    for key in dic_var: #assigns '!' to sorted variable by scanning each element
        if key in sorted_variable_without_not: #if element is in common with key
            placement_of_not = dic_var.get(key) - 1  #assign value of occurrence - 1 which helps to locate the last position of key in string by adding with index_of_not_var
            while dic_var.get(key) != 0: #stops when all '!' of a key are assigned
                index_of_not_var = sorted_variable_without_not.find(key) #find index of first occurrence of '!' letter
                sorted_variable_without_not = sorted_variable_without_not[:index_of_not_var + placement_of_not] + '!' + sorted_variable_without_not[index_of_not_var + placement_of_not:]
                #places '!' starting from the last of key to first of key, example : ccc --> cc!c --> c!c!c --> !c!c!c
                placement_of_not -= 1
                dic_var[key] -= 1
    return sorted_variable_without_not  #returns the variables arranged by alphabetical order
def sort_problem(problem):
    problem = problem.split() #split by using space to locate each terms
    for variable in problem:
        index = problem.index(variable) #find index of the terms to access problem[index]
        if variable != '+':
            problem[index] = sort_variable(variable) #sorts the term with sort_variable function
    return ' '.join(problem) #returns the string of sorted problem

def return_str_of_not(pos,variables): #position is used to access characters in the variables
    not_var = ''.join([variables[pos][i + 1] for i in range(len(variables[pos]) - 1) if variables[pos][i] == '!'])
    #filters out such that only characters that has '!' in front of it is being stored by locating '!' and return variable behind '!'
    #returns a string of '!' variables without '!'
    return not_var
def return_str_without_not(pos,not_var,variables): #not_var is the string returned by return_str_of_not, which contains '!' variables
    var = ''.join([letter for letter in variables[pos] if not letter in not_var]).replace('!','')
    #filters out the characters in common with not_var and removes '!' to find variables that does not have '!' infront of them
    return var

def single_variable_theorem_or(problem):
    variables = problem.split()  #split into term, '+', term2 to access each terms
    if variables[0] == variables[2]:  #Case 1: a + a = a
        variables.pop(2) #removes the second variable
    elif variables[0] == '1' or variables[2] == '1':  #Case 2: a + 1 = 1
        variables = ['1']
    else:
        not_var1 = return_str_of_not(0, variables)  #'!' elements of first term
        not_var2 = return_str_of_not(2, variables)  #'!' elements of second term
        var1 = return_str_without_not(0, not_var1, variables)  #elements of first term
        var2 = return_str_without_not(2, not_var2, variables)  #elements of second term
        if variables[0] == '0' or variables[2] == '0':  #Case 3: a + 0 = a
            variables = [var for var in variables if var != '0'] #terms are removed if it's '0'
        elif (var1 == not_var2) and (var2 == not_var1): #check if the variables are inverse of each other, example: !abc + a!b!c
            unique_var = sorted(list(set(not_var1) | set(not_var2) | set(var1) | set(var2))) #return sorted list of unique characters in the problem
            if len(var1 + var2 + not_var2 + not_var1) == 2: #Case 4: x + !x = 1
                variables = ['1']
            elif not var1 or not var2: #XNOR scenario, where if 1 of the term has no '!' in all of its character : !A!B + AB = A XNOR B
                variables = [] #list to contain the new terms
                for index,var in enumerate(unique_var): #loop over each unique characters in problem
                    variables.append(var) #adds the unique variables to list
                    if index != len(unique_var) - 1: #makes it so it stops adding ' XNOR ' after it reaches last element
                        variables.append(' XNOR ') #adds XNOR
            else: #XOR scenario, since the variables are inverse of each others, and it's not XNOR or Case 4: x + !x = 1, it must be XOR
                variables = []
                for index, var in enumerate(unique_var): #same approach as XNOR scenario
                    variables.append(var)
                    if index != len(unique_var) - 1:
                        variables.append(' XOR ')
        elif (len(not_var1 + var1) == 1 and len(not_var2 + var2) != 1) or (len(not_var1 + var1) != 1 and len(not_var2 + var2) == 1):
            #checks if 1 of the terms is 1 character while other term is more than 1 character
            #to use absorptive law on problems like : !a + ab = !a + b
            #scenarios like !a!b + !a!bc is done before this function was used, through factorising to !a!b(1 + c), hence it's to filter this out
            variables = absorptive_law(problem) #if condition is met, variables goes through absorptive law
    if variables [-1] == '+': #if the last term got eliminated to due to Case 1: a + a = a
        return variables[:-1] #it returns only the first term
    elif variables [0] == '+': #if first term is '0' and got eliminated
        return variables [1:] #returns only second term
    else:
        return variables #return simplified problem that went through 'OR'
def absorptive_law(variables):
    absorption = False
    variables = variables.split() #!h , + , !hady
    not_var1 = return_str_of_not(0, variables)  # Not elements of first variable C
    not_var2 = return_str_of_not(2, variables)  # Not elements of second variable D
    var1 = return_str_without_not(0, not_var1, variables)  # elements of first variable that is not 'not' D
    var2 = return_str_without_not(2, not_var2, variables)  # elements of second variable that is not 'not' C
    if len(not_var1 + var1) > len(not_var2 + var2):
        smaller = variables[2]
        bigger = variables[0]
    if len(not_var1 + var1) < len(not_var2 + var2):
        smaller = variables[0]
        bigger = variables[2]
    smaller_without_not = smaller.replace('!','') #takes away '!'
    if smaller_without_not in bigger:
        absorption = True
    if absorption == True:
        index_of_absorption = bigger.find(smaller_without_not)  # finds index of absorption
        if smaller_without_not != smaller: #smaller term has '!'
            if index_of_absorption > 0 and bigger[index_of_absorption - 1] == '!':  # if second term has 'not'
                variables = smaller
            elif index_of_absorption > 0 and bigger[index_of_absorption - 1] != '!': #if second term has no 'not'
                bigger = bigger[:index_of_absorption] + bigger[index_of_absorption + 1:]
                variables = smaller + '+' + bigger
            elif index_of_absorption == 0:
                bigger = bigger[index_of_absorption+1:]
                variables = smaller + '+' + bigger
        elif smaller_without_not == smaller: #smaller term has no '!'
            if index_of_absorption > 0 and bigger[index_of_absorption - 1] != '!':  # if second term no 'not'
                variables = smaller
            elif index_of_absorption > 0 and bigger[index_of_absorption - 1] == '!':  # if second term has 'not'
                bigger = bigger[:index_of_absorption-1] + bigger[index_of_absorption + 1:]
                variables = smaller + '+' + bigger
            elif index_of_absorption == 0:
                variables = smaller
    return variables

def single_variable_theorem_and(var):
    if not var == '1': # Case 1: A.1 = A
        var = var.replace('1', '')
    if '0' in var:  # Case 2: A.0 = 0
        var = '0'
    return sort_variable(complement_law(var))  # returns sorted of Case 3: A.!A = 0 and Case 4: A.A = A
def complement_law(var):
    position_of_not_var = []  # position of '!' variables
    index = var.find('!') # find index of '!'
    while index != -1:  # scan until no more '!'
        position_of_not_var.append(index + 1)  # add index of character after '!' to list of position
        index = var.find('!', index + 1) # find position of next '!' character
    var_without_not_variables = ''.join([var[i] for i in range(len(var)) if i not in position_of_not_var]).replace('!', '')
    #only variables that does not have '!' in front
    var_without_not_variables = set(var_without_not_variables)  # Case 4: A.A = A, filter out duplicates
    not_variables = ''.join(var[i] for i in position_of_not_var)  #Only not variables
    not_variables = set(not_variables) #filter out duplicates, !A.!A = !A
    if set(var_without_not_variables) & set(not_variables): #Case 3 !A.A = 0, meaning if not_variables and variables intercept, case applies
        var = '0'
    elif not_variables:  # if Case 3: !A.A = 0 not applicable, return Case 4: A.A = A
        var = '!' + '!'.join(not_variables) + ''.join(var_without_not_variables)  # if there is '!' variables
    else:
        var = ''.join(var_without_not_variables)  # if there is no '!' variable
    return var

def simplify_using_single_variable_theorem(problem):
    problem = problem.split()
    for index, var in enumerate(problem):
        if var != '+': #filters out '+' to apply AND theorem on terms
            problem[index] = single_variable_theorem_and(var) #Simplify SOP terms
            problem[index] = problem[index].replace(' ','')
    problem = rejoin_expression(single_variable_theorem_or(' '.join(problem))) #simplify entire expression with OR theorems then join string

    return problem
def rejoin_expression(problem): #to rearrange spaces in the problem
    result = []
    for ch in problem: #adds space before and after '+'
        if ch == '+':
            result.append(' + ')
        else:
            result.append(ch)
    return ''.join(result).strip()

def find_common_factors (problem):
    problem = problem.split() #split into terms to access each
    not_var1 = return_str_of_not(0,problem) #'!' variables of term 1
    not_var2 = return_str_of_not(2,problem) #'!' variables of term 2
    var1 = return_str_without_not(0,not_var1,problem) #variables of term 1
    var2 = return_str_without_not(2,not_var2,problem) #variables of term 2
    common_not_factors = list(set(not_var1) & set(not_var2)) #find factors that are '!', through sets
    common_not_factors = ''.join('!' + letter for letter in common_not_factors) #return string of factors that are '!'
    common_factors =  ''.join(list(set(var2) & set(var1))) #return string of factors without '!', through sets
    common_factors = sort_problem(common_factors + common_not_factors) #joins both strings together and sort them

    return common_factors
def factorisation(problem,factor):
    variables = problem.split()
    not_var1 = return_str_of_not(0, variables) #'!' variables of term 1
    not_var2 = return_str_of_not(2, variables) #'!' variables of term 2
    var1 = return_str_without_not(0, not_var1, variables) #variables of term 1
    var2 = return_str_without_not(2, not_var2, variables) #variables of term 2
    remaining_of_not_var1 = ['!' + letter for letter in not_var1 if letter not in factor] #list of '!' variables of term 1 that are not in factor
    remaining_of_not_var2 = ['!' + letter for letter in not_var2 if letter not in factor] #list of '!' variables of term 2 that are not in factor
    remaining_of_var1 = [letter for letter in var1 if letter not in factor] #list of variables of term 1 that are not in factor
    remaining_of_var2 = [letter for letter in var2 if letter not in factor] #list of variables of term 2 that are not in factor
    final_var1 = sort_problem(''.join(remaining_of_not_var1 + remaining_of_var1)) #joins remaining of variables of term 1 together as a string
    final_var2 = sort_problem(''.join(remaining_of_not_var2 + remaining_of_var2)) #joins remaining of variables of term 2 together as a string
    if not final_var1: #if string is empty, puts 1, since A + AB = A(1+B)
        final_var1 = '1'
    if not final_var2:
        final_var2 = '1'
    problem = factor + '(' + final_var1 + ' + ' + final_var2 + ')'

    return problem
def factorise_problem(problem):
    if len(problem.split()) >= 3:  # checks if problem requires factorising, through checking length of problem, as it is split into term1 , + , term2
        factor = find_common_factors(problem) #returns common factor : ABC + AB, common factor is AB
        if factor:
            problem = factorisation(problem, factor)  #returns a string with factor : ABC + AB = AB(C + 1)

    return problem #return factorised form

def extract_terms_in_bracket(problem):
    #used after factorisation
    index_of_opening_bracket = problem.find('(') #finds index of opening bracket
    index_of_closing_bracket = problem.find(')') #finds index of closing bracket
    terms_in_bracket = problem[index_of_opening_bracket+1:index_of_closing_bracket] #find terms in brackets through using index of brackets
    return terms_in_bracket #return terms in brackets
def put_simplified_terms_in_brackets_back(terms,factorised_problem):
    index_of_opening_bracket = factorised_problem.find('(') #finds index of opening brackets
    problem_with_simplified_terms_in_brackets = factorised_problem[:index_of_opening_bracket] + '(' + terms + ')'
    #track terms outside of bracket using index of opening bracket, then combine with terms in bracket

    return problem_with_simplified_terms_in_brackets
def final_simplification(simplified_terms,problem_with_simplified_terms_in_bracket):
    #used for simplifying in 2 scenarios after factorising
    #AB(1) = AB
    #AB(0) = 0
    index_of_opening_bracket = problem_with_simplified_terms_in_bracket.find('(')
    index_of_closing_bracket = problem_with_simplified_terms_in_bracket.find(')')
    if simplified_terms == '1':#if terms in bracket is 1, result is the factor
        final_problem = problem_with_simplified_terms_in_bracket[:index_of_opening_bracket]
    elif simplified_terms == '0': #if terms in bracket is 0, result is 0
        final_problem = '0'
    else:
        final_problem = problem_with_simplified_terms_in_bracket
    return final_problem

def simplification_process(case_sensitivity,problem):
    if case_sensitivity == 'n': #checks if user wants case sensitivity
        problem = problem.lower()
    if check_for_error(problem) == 'single': #if problem involves single term , such as A!A
        if not '+' in problem[0]:
            print(f'The simplified problem is: {single_variable_theorem_and(problem)}')
        else:
            print('Please input a proper problem')
    elif check_for_error(problem) == 'pass': #if problem passes error checks
        simplified_problem = simplify_using_single_variable_theorem(problem)
        print(f'Simplify with single variable theorems and sort into alphabetical order')
        print(f'{problem} = {simplified_problem}')
        print(f'\nFactorising problem')
        factorised_problem = factorise_problem(simplified_problem)
        if factorised_problem == simplified_problem: #if problem can't be further factorised and simplified
            print(f'No common factors.')
            print(f'\nFinal expression: {simplified_problem}')
        else: #if problem can be further factorised and simplified
            print(f'{simplified_problem} = {factorised_problem}') #returns factorised problem
            terms_in_bracket = extract_terms_in_bracket(factorised_problem)
            simplified_problem_in_bracket = simplify_using_single_variable_theorem(extract_terms_in_bracket(factorised_problem))
            print('\nSimplify terms within brackets')
            print(f'{terms_in_bracket} = {simplified_problem_in_bracket}') #shows simplification of terms in bracket
            print('\nPut simplified terms into bracket') #places simplified terms back into bracket
            problem_with_simplified_terms_in_bracket = put_simplified_terms_in_brackets_back(simplified_problem_in_bracket,factorised_problem)
            print(f'{factorised_problem} = {problem_with_simplified_terms_in_bracket}')

            if 'XOR' in problem_with_simplified_terms_in_bracket or 'XNOR' in problem_with_simplified_terms_in_bracket:
                #it means XNOR or XOR terms in bracket, meaning fully simplified
                print(f'\nFinal expression: {problem_with_simplified_terms_in_bracket}')
            else: #checks for possible further simplifications, like AB(1) = AB, AB(0) = 0
                print(f'\nFinal expression: ')
                final_expression = final_simplification(simplified_problem_in_bracket,problem_with_simplified_terms_in_bracket)
                print(f'{final_expression}')
    else: #if there is error with input
        print(check_for_error(problem))
def main():
    check_for_case_sensitivity = ''
    exit_program = ''
    print(f'Only 2 terms are allowed')
    print(f'No brackets are allowed')
    print(f'Example of input: abcd + !ab!cd\n')
    while check_for_case_sensitivity not in ('y', 'n'): #repeatedly ask for case sensitivity input until y or n is typed
        check_for_case_sensitivity = input("Enable case-sensitivity? (y/n)\n").lower() #accept capital and lowercase
    if check_for_case_sensitivity == 'y':
        print('Case sensitivity: True')
    else:
        print('Case sensitivity: False')
    while exit_program != 'y': #loops until user types y at exit program
        problem = input("\nEnter the problem to solve: ")
        simplification_process(check_for_case_sensitivity,problem)
        exit_program = input("\nPress 'y' if you wish to exit\n").lower() #accept capital and lowercase

main()