try:
    from .AND_simplification import *
    from .identify_variables import *
except ImportError:
    from AND_simplification import *
    from identify_variables import *

def or_simplification(problem, print_check = False):
    """
    Performs OR simplification logic basic laws, absorptive law, consensus theorems after performing AND simplification on each terms.

    Algorithm:
        AND simplification: Split up expression into terms, and simplify individually logic helper function: AND_simplification.
        Remove duplicate terms: Create a new list and append the terms towards the new list, filtering out duplicate terms
        Single variable complement law: Create a new list and append the terms towards the new list after removing '!', then deduplicate the list. Catches 'A','!A' which equates to 1
        Absorptive law: Apply absorptive law to the expression logic helper function: absorptive_law()
        Consensus theorem: Apply consensus theorem to the expression logic helper function: consensus_theorem()

    Args:
        problem (str): Problem to be simplified.
        print_check (bool): If true, it prints out the working. Meant for debugging/showcase of working.

    Returns:
        str: Simplified expression after OR simplifications.

    Example:
        or_simplification('!AX + !CA + !CX', print_check=True) returns '!AX + !CA'.
        Working: !AX + !CA + !CX = !AX + !CA (Consensus theorem 3: !CX is redundant)
    """
    red = '\033[91m'
    blue = '\033[34m'
    end = '\033[0m'
    #Cosmetic-----------------------------------

    terms = identify_terms(problem) #create a list of terms in the problem.
    simplified_terms = []
    for term in terms:
        term = and_simplification(term)
        if term not in simplified_terms: #remove duplicates, A + A = A
            simplified_terms.append(term)

    simplified_terms_without_zeros = [term for term in simplified_terms if term != '0'] #remove 0's after AND simplification.
    if len(simplified_terms_without_zeros) == 1: #Only 1 term left after simplification.
        if print_check and problem != simplified_terms_without_zeros[0]: #for printing.
            print(f'{problem} = {' + '.join(simplified_terms)} {blue}(Simplified with AND theorems){end}')
            print(f'= {simplified_terms_without_zeros[0]}')
        return simplified_terms[0]
    elif print_check and ' + '.join(simplified_terms) != problem: #for printing, if simplification took place.
        print(f'{problem} = {' + '.join(simplified_terms)} {blue}(Simplified with AND theorems){end}')

    check_complement_law = []
    for each_term in simplified_terms:
        term_without_not = each_term.replace('!','') #removes '!' to check whether the term is single variable.
        if len(term_without_not) == 1: #single variable term like '!A', 'A'
            check_complement_law.append(term_without_not)
        if len(list(set(check_complement_law))) != len(check_complement_law): #There is 2 terms like '!A', 'A', thus simplifies to 1. 'A + !A = 1'. 'A + A' cannot exist, as it has been filtered out earlier.
            if print_check:
                print(f'{problem} = 1')
            return '1'

    if '1' in simplified_terms: #1 + A = 1
        return '1'
    elif '0' in simplified_terms: #0 + A = A
        simplified_terms.remove('0')

    simplified_terms = absorptive_law(simplified_terms,print_check) #apply absorptive laws.

    simplified_terms = consensus_theorem(simplified_terms,print_check) #apply consensus theorems.

    simplified_exp = ' + '.join(simplified_terms) #convert simplified expression into a string.

    if simplified_exp == problem: #cannot simplify anymore.
        return simplified_exp
    else: #recursive OR simplification
        return or_simplification(simplified_exp,print_check)


def absorptive_law(terms,print_check = False):
    """
    Apply absorptive law to terms.

    Args:
        terms (list): terms in the problem
        print_check (bool): if true, it prints out the working. Meant for debugging/showcase of working.

    Returns:
        list: the simplified terms after absorptive laws.

    Example:
        absorptive_law(['A','ABC','ADF']) returns ['A'].
    """
    red = '\033[91m'
    blue = '\033[34m'
    end = '\033[0m'
    #Cosmetic-----------------------------------

    common_var_all_terms = find_common_variables(terms) #common variable among all the terms

    if any(common_var_all_terms == term for term in terms): #checks if common variable is 1 of the term
        if print_check:
            problem = ' + '.join(terms)
            problem = problem.replace(common_var_all_terms,f'{red}{common_var_all_terms}{end}')
            print(f'{problem} = {red}{common_var_all_terms}{end} {blue}(Absorptive law){end}')
        return [common_var_all_terms]

    absorbed = classic_absorptive_law(terms,print_check) #for checking absorptive law individually
    return absorbed

def classic_absorptive_law(terms,print_check = False):
    """
    Check for absorptive laws between all pairs of the term, by looping them with each other.

    Args:
        terms (list): terms in the problem
        print_check (bool): if true, it prints out the working. Meant for debugging/showcase of working.

    Returns:
        list: the simplified terms after absorptive laws.

    Example:
        classic_absorptive_law(['A','BC','C','CD','ABCD'],print_check=False) returns ['A','C'].
        ABCD gets absorbed by A, BC & CD gets absorbed by C.
    """
    red = '\033[91m'
    blue = '\033[34m'
    yellow = '\033[93m'
    purple = '\033[95m'
    pink = '\033[38;5;205m'
    end = '\033[0m'
    colors = [red,blue,yellow,purple,pink]
    #Cosmetic---------------------------------------------------

    removed_vars = [] #List of terms that were absorbed/replaced by ''
    absorped_vars = [] #List of terms that remain after absorption.

    new_terms = terms.copy()

    #Loop each terms against other term
    for i, term1 in enumerate(terms):
        for j in range(i + 1, len(terms)):
            term2 = terms[j]
            if not term2 in removed_vars or not term1 in removed_vars: #ensure at least 1 term that is not removed is being processed.
                term_test = [term1, term2]
                common_var_two_terms = find_common_variables(term_test) #find common variables between the 2 terms.
                if common_var_two_terms == term1:
                    #A + AB = A + ''
                    new_terms[i] = common_var_two_terms
                    new_terms[j] = ''
                    removed_vars.append(term2)
                    absorped_vars.append(term1)
                if common_var_two_terms == term2:
                    #AB + A = '' + A
                    new_terms[j] = common_var_two_terms
                    new_terms[i] = ''
                    removed_vars.append(term1)
                    absorped_vars.append(term2)

    new_terms = [term for term in new_terms if term != ''] #new terms after absorptive law.

    if new_terms != terms and print_check == True:
        #for printing to debug/show working.
        print_new_terms = new_terms.copy()
        print_terms = terms.copy()
        absorptive_var = []
        taken_terms = []
        var_dic = {}

        for var in absorped_vars:
            if var not in absorptive_var:
                absorptive_var.append(var) #remove duplicates

        for count,absorbed_var in enumerate(absorptive_var):
            if absorbed_var not in var_dic: #create dictionary of distinct absorptive variables.
                var_dic[absorbed_var] = []
            for i,term in enumerate(print_terms):
                if absorbed_var in term and term not in taken_terms:
                    index = term.index(absorbed_var)
                    if index == 0 or term[index - 1] != '!': #ensure it's not a not_var, such as '!A'.
                        taken_terms.append(term)
                        if absorbed_var != term:
                            var_dic[absorbed_var].append(term) #store the term affected inside dictionary sector labelled as 'absorbed_var'.

        var_dic_copy = var_dic.copy()
        for var in var_dic_copy.keys():
            if not var_dic[var]: #if no terms affected by the absorptive variable, pop it.
                var_dic.pop(var)

        for absorb_var,terms in var_dic.items():
            count = list(var_dic.keys()).index(absorb_var) #position of current absorbed variable in dictionary keys, to choose color for printing.
            for i,term in enumerate(print_terms):
                if absorb_var == term or term in terms:
                    print_terms[i] = f'{colors[count % 5]}{term}{end}'

        for i,term in enumerate(print_new_terms):
            if term in list(var_dic.keys()):
                count = list(var_dic.keys()).index(term) #position of current absorbed variable in dictionary keys, to choose color for printing.
                print_new_terms[i] = f'{colors[count % 5]}{term}{end}'

        print_terms = ' + '.join(print_terms)
        print_new_terms = ' + '.join(print_new_terms)
        print(f'{print_terms} = {print_new_terms} {blue}(Absorptive law){end}')

    return new_terms

def consensus_theorem(terms,print_check = False):
    """
    Applies the Consensus Theorem and related redundancy simplifications to a list of Boolean terms.

    This function scans through the given Boolean terms and attempts to simplify them by:
        1. Applying the Consensus Theorem for terms with complementary variables (e.g. !AB + AB → B).
        2. Detecting redundant literals within terms (e.g. !AX + AC + XC -> !AX + AC).
        3. Removing extra literals like X!X that do not contribute to simplification.
        4. Optionally prints step-by-step simplification logic color-coded output for demonstration/debugging.

    Args:
        terms (list of str): Terms to be simplified
        print_check (bool): If True, prints the working with color highlights. Default is False.

    Returns:
        list of str: The simplified list of Boolean terms after applying the consensus theorem and redundancy removal.

    Example:
        consensus_theorem(['!AX','!CA','!CX'],print_check=False) returns ['!AX', '!CA'].
    """
    red = '\033[91m'
    blue = '\033[34m'
    end = '\033[0m'
    #Cosmetic---------------------------------------------------------
    complements = find_complements(terms) #find all the complements inside the problem

    if len(complements) == 0: #if no complements, consensus theorem unapplicable
        return terms

    complements_freq = {} #dictionary to store complements

    #stores all the complements of a term as a dictionary.
    for term in terms: #loops over each terms
        matched_complements = [comp for comp in complements if comp in term]
        if matched_complements:
            complements_freq[term] = matched_complements
        else:
            complements_freq[term] = ''

    simplifiable_terms = [key for key,value in complements_freq.items() if value != ''] #terms that may be simplified with complement

    for term in simplifiable_terms:
        #simplify a single complement variable and return simplified list if there is a variable like !X or X
        if len(complements_freq[term]) == 1: #terms with only 1 complement
            variable = complements_freq[term][0] #define variable, like 'X'
            complement_of_variable = '!' + variable #define not_variable like '!X'

            new_terms = [t.replace(complement_of_variable, '') for t in terms]  # removes '!X' first
            new_terms = [t.replace(variable, '') for t in new_terms]  # removes 'X'

            for i, new_term in enumerate(new_terms):
                if not new_term:  # single variable like '!X'
                    new_terms[i] = terms[i] #new_terms[i] gets assigned the single variable

                    if print_check and terms != new_terms:

                        affected_terms = [term for term in terms if complements_freq.get(term) and variable in complements_freq[term]] #return terms affected by complement
                        affected_terms_index = [terms.index(term) for term in terms if term in affected_terms]

                        terms_print = [f'{red}{term}{end}' if term in affected_terms else term for term in terms] #color affected terms
                        terms_print = ' + '.join(terms_print)
                        new_terms_print = [f'{red}{term}{end}' if i in affected_terms_index else term for i,term in enumerate(new_terms)]
                        new_terms_print = ' + '.join(new_terms_print)
                        print(f'{terms_print} = {new_terms_print} {blue}(Consensus theorem 1){end}')

                    return new_terms #simplified after consensus theorem

    #if something like !AB + AC, it tries to find redundancy
    for complement in complements:
        similar_terms = [term for term in terms if complement in ''.join(complements_freq[term])] #list of term that has same complements.

        common_var_of_similar_terms = find_common_variables(similar_terms)

        for similar_term in similar_terms:
            similar_terms_removed_complements = [t.replace('!' + complements_freq[similar_term][0], '') for t in similar_terms] #removes '!X'
            similar_terms_removed_complements = [t.replace(complements_freq[similar_term][0], '') for t in similar_terms_removed_complements] #removes 'X'

        if all(common_var_of_similar_terms == term for term in similar_terms_removed_complements):
            #if their remaining is common variable after removal of complements, like !AB + AB, means consensus theorem applicable
            index_affected_terms = [i for i,term in enumerate(terms) if term in similar_terms and common_var_of_similar_terms in term] #indexes of terms which can be simplified.
            new_terms = [common_var_of_similar_terms if i == index_affected_terms[0] else term for i,term in enumerate(terms)] #replace first term with simplified common variable
            new_terms = [term for i,term in enumerate(new_terms) if i != index_affected_terms[1]] #remove the 2nd term affected, as it is redundant after simplification

            if print_check:
                terms_print = [f'{red}{term}{end}' if term in similar_terms else term for term in terms]
                terms_print = ' + '.join(terms_print)
                new_terms_print = [f'{red}{term}{end}' if i == index_affected_terms[1]-1 else term for i,term in enumerate(new_terms)]
                new_terms_print = ' + '.join(new_terms_print)
                print(f'{terms_print} = {new_terms_print} {blue}(Consensus theorem 2){end}')

            return new_terms

        else:  # consensus theorem fails, extract literals and reduce redundancy, !AX + AC + XC = !AX + AC --> XC is redundant
            extra_literal = sort_term(''.join(similar_terms_removed_complements)) #redundant term
            terms_to_remove = []
            for term in terms:
                if extra_literal in term and complement not in term: #term is possibly redundant since extra_literal is in it, and no complement
                    index = term.index(extra_literal)
                    if index > 0 and term[index-1] != '!': #term is redundant if there is no '!' in front of it and index > 0
                        terms_to_remove.append(term)
                    elif index == 0:
                        terms_to_remove.append(term)
            new_terms = [term for term in terms if term not in terms_to_remove]

            not_var, var = identify_variables(extra_literal)
            valid_literal = False

            if ' + '.join(terms) != ' + '.join(new_terms):
                valid_literal = True
            if len(not_var) == 1 and len(var) == 1: #flags out terms like 'X!X'
                if not_var[0].replace('!','') == var[0]:
                    valid_literal = False

            if print_check == True and valid_literal == True: #prevent redundancy such as X!X from passing the check
                terms_print = []
                #not_var, var = identify_variables(extra_literal)
                for term in terms:
                    if term in similar_terms:
                        colored_term = term #make copy
                        index_of_colored_term = term.index(complement)
                        colored_term = colored_term.replace(f'!{complement}', f'{red}!{complement}{end}')
                        if index_of_colored_term == 0 or term[index_of_colored_term -1] != '!':
                            colored_term = colored_term.replace(complement, f'{red}{complement}{end}')
                        for each_not_var in not_var:
                            colored_term = colored_term.replace(each_not_var, f'{blue}{each_not_var}{end}')
                        for each_var in var:
                            colored_term = colored_term.replace(each_var, f'{blue}{each_var}{end}')
                        terms_print.append(colored_term)
                    else:
                        #print(terms)
                        term = term.replace(extra_literal, f'{blue}{extra_literal}{end}')
                        terms_print.append(term)

                new_terms_print = [f'{red}{term}{end}' if term in similar_terms else term for term in new_terms]
                terms_print = ' + '.join(terms_print)
                new_terms_print = ' + '.join(new_terms_print)
                print(f'{terms_print} = {new_terms_print} {blue}(Consensus theorem 3: {extra_literal} is redundant){end}')

            return new_terms


if __name__ == '__main__':
    print(or_simplification('!AX + !CA + !CX', print_check=True))
    #print(consensus_theorem(['!AX','!CA','!CX'],print_check=False))

