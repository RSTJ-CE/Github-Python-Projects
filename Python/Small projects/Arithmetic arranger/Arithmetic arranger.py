def problem_parts(problem):
    character = ''
    parts = []
    for char in problem:  # finding numbers
        if char != ' ':
            character += char
        elif char == ' ':  # if character not empty, append
            parts.append(character)
            character = ''
    if character:  # if last character not empty, it appends
        parts.append(character)
    return (parts)


def check_errors_in_problems(parts, problems):
    #check for errors as a whole
    if len(problems) > 5:  # too many problems
        return 'Error: Too many problems.'
    operator = parts[1]
    numbers = list(filter(lambda number: number.isdigit(), parts))
    if operator != '+' and operator != '-':  # operator error
        return "Error: Operator must be '+' or '-'."

    if not parts[0].isdigit() or not parts[2].isdigit():  # check if there letters
        return 'Error: Numbers must only contain digits.'

    for number in numbers:  # big number
        if int(number) >= 10000:
            return 'Error: Numbers cannot be more than four digits.'
    return None


def find_line(parts, problems, choosen_line):
    length_of_first_operand = len(parts[0])
    length_of_second_operand = len(parts[2])
    higher = max(length_of_first_operand, length_of_second_operand)  # find higher index
    lower = min(length_of_first_operand, length_of_second_operand)  # find lower index
    dashes = higher + 2
    space_for_lower_operand = (higher - lower) + 1

    if length_of_first_operand >= length_of_second_operand:  # adding of space infront higher
        line_1 = '  ' + parts[0]
        line_2 = parts[1] + ' ' * space_for_lower_operand + parts[2]
    else:
        line_1 = ' ' * (space_for_lower_operand + 1) + parts[0]
        line_2 = parts[1] + ' ' + parts[2]
    line_3 = '-' * dashes
    if choosen_line == 1:
        return (line_1)
    elif choosen_line == 2:
        return (line_2)
    elif choosen_line == 3:
        return (line_3)


def calculate(parts, problem):
    operator = parts[1]
    length_of_first_operand = len(parts[0])
    length_of_second_operand = len(parts[2])
    higher = max(length_of_first_operand, length_of_second_operand)
    lower = min(length_of_first_operand, length_of_second_operand)
    num1 = int(parts[0])
    num2 = int(parts[2])
    spacing = (higher + 2) - len(str(num1 + num2))  # spacing
    if operator == '+':  # addition
        return ' ' * spacing + str(num1 + num2)
    elif operator == '-':  # subtraction
        if '-' in str(num1 - num2):
            return ' ' * (spacing - 1) + str(num1 - num2)  # account for negative sign
        else:
            return ' ' * spacing + str(num1 - num2)


def arithmetic_arranger(problems, show_answers=False):
    line_1 = []
    line_2 = []
    line_3 = []
    calculation = []
    line_4 = []
    for problem in problems:
        error = check_errors_in_problems(problem_parts(problem), problems)
        if error:  # check for errors
            return error
        line_1.append(find_line(problem_parts(problem), problems, 1))
        line_2.append(find_line(problem_parts(problem), problems, 2))
        line_3.append(find_line(problem_parts(problem), problems, 3))
        if show_answers == False:
            converted_form = '    '.join(line_1) + '\n' + '    '.join(line_2) + '\n' + '    '.join(line_3)
        elif show_answers == True:
            pass
            result = calculate(problem_parts(problem), problem)
            line_4.append(result)
            converted_form = '    '.join(line_1) + '\n' + '    '.join(line_2) + '\n' + '    '.join(
                line_3) + '\n' + '    '.join(line_4)
    return converted_form

def ask_for_answer():
    prompt_to_show_ans = input(f'Would you like answer to be shown?(y/n)')
    if prompt_to_show_ans.lower() == 'y':
        show_ans = True
    else:
        show_ans = False
    return show_ans

def input_problems():
    problems = []
    count = 0
    print(f'Enter problem, enter "n" to stop')
    while not 'n' in problems and count != 5:
        problem = ''
        while check_for_error_input(problem) != 'problem accepted\n' and problem != 'n':
            problem = input(f'Please enter problem {count + 1}: ')
            print(check_for_error_input(problem))
        problems.append(problem)
        count += 1
    if problems[-1] == 'n':
        problems.pop(-1) #removes 'n'
    return problems

def check_for_error_input(problem):
    operands = problem.split(' + ')
    number_of_operands = len(operands)
    if problem == 'n':
        return 'problem accepted\n'
    if number_of_operands > 2:
        return 'Only 2 operands are accepted\n'
    if ' + ' not in problem:
        return 'Ensure correct format\n'
    if not ''.join(operands).isdigit():
        return 'Only digits are accepted\n'
    return 'problem accepted\n'

def main():
    print(f'Arithmetic arranger only accepts up to 5 problems')
    print(f"Only accepts '+' or '-'")
    print(f'Maximum operands digits: 4\n')
    problems = input_problems()
    number_of_problems = len(problems)
    if number_of_problems == 0:
        print(f'Invalid input')
    else:
        print(arithmetic_arranger(problems,ask_for_answer()))

main()
