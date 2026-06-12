try:
    from .identify_variables import *
except ImportError:
    from identify_variables import *


def and_simplification(term):
    """
    Perform AND simplification on the term
    Purpose is to simplify the term logic AND theorems.

    Args:
        term (str): single term

    Returns:
        str : simplified term after AND theorems.

    Example:
        Example 1: and_simplification('CBA!ADE') returns '0'. Because 'A','!A' are both in the term.
        Example 2: and_simplification('ABCABCABC') returns 'ABC'.
    """
    not_var,var = identify_variables(term)
    common_var = set(''.join(not_var)).intersection(''.join(set(var)))
    #not_var and var is in common, A!A = 0
    if term == '1':
        return '1'
    if term == '!0':
        return '1'
    if term == '!1':
        return '0'
    if common_var:
        return '0'

    term = term.replace('!0','')
    term = term.replace('!1','0')
    term = term.replace('1','')
    if '0' in term:
        term = '0'

    term = sort_term(term)
    return term

if __name__ == '__main__':
    term = '!ABA!B'
    print(and_simplification(term))