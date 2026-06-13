import tkinter as tk
import sys
from tkinter import ttk, scrolledtext

from logic.Error_handling import handle_input_error
from logic.solver import main


root = tk.Tk()
root.title('Boolean Algebra Solver')
root.resizable(True, True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f'{800}x{800}+{int(screen_width/2-800/2)}+{int(screen_height/2-800/2)}')

root.rowconfigure(0,weight=1) #Rules label
root.rowconfigure(1,weight=1) #Prompt
root.rowconfigure(2,weight=1) #Input widget
root.rowconfigure(3, weight=1) #enter button
root.rowconfigure(4,weight=1) #Solution label
root.rowconfigure(5,weight=1) #Solution widget
root.rowconfigure(6,weight=1)
root.columnconfigure(0,weight=2)
root.columnconfigure(1,weight=1)

#User input
Title_label = ttk.Label(root, text='Boolean Algebra Solver', font=('Arial',20,'bold'),foreground='red')
Rules_label = ttk.Label(root, text="Rule 1: No brackets\nRule 2: 'Not' denoted with '!'\nExample input: A!B + AB!C", font=('Arial', 20, 'bold'))
user_input_label = ttk.Label(text='Problem', font=('Arial', 20, 'bold'),foreground='red')
user_input = tk.Text(root, width=1, height=5)
enter_button = ttk.Button(root, text='Enter', command=lambda: display_info())

#Processing
problem_label = ttk.Label(root,text=f'Solution', justify='left', font=('Arial', 20, 'bold'),foreground='red')

#After processing
ProblemSolutionText = scrolledtext.ScrolledText(root,height=12)
AlgorithmLabel = ttk.Label(text='Algorithm', font=('Arial', 20, 'bold'),foreground='red')
Algorithm = scrolledtext.ScrolledText(root,height=15)

class RedirectWorking: #Class to transfer print output in terminal to widget
    def __init__(self,widget):
        self.widget = widget

    def write(self,text):
        colors = ['\033[91m','\033[34m','\033[93m','\033[95m','\033[38;5;205m','\033[0m','\033[38;5;34m']
        for color in colors:
            text = text.replace(color,'')
        self.widget.insert("end", text) #insert text at the end
        self.widget.see("end") #scroll text widget to the end

    def flush(self):
        pass

def display_info():
    #delete previous inputs
    ProblemSolutionText.delete(1.0, tk.END)
    Algorithm.delete(1.0, tk.END)

    #direct output from terminal to text widget
    sys.stdout = RedirectWorking(Algorithm)
    problem = user_input.get('1.0', 'end-1c')
    if handle_input_error(problem):
        ProblemSolutionText.insert("end",'Follow the correct format for input')
        return

    problem = problem.replace(' ', '').replace('+', ' + ') #Reformat '+' into suitable format once it passes check

    ProblemSolutionText.insert("end", f'\n\nProblem = {problem}')
    sorted_problem, solution = main(original_problem=problem,print_check=True)
    ProblemSolutionText.insert("end", f'\n\nSorted problem = {sorted_problem}')
    ProblemSolutionText.insert("end", f'\n\nSimplified problem = {solution}')

Title_label.grid(row=0, column=0,columnspan=2, sticky="n", padx=10, pady=10)
Rules_label.grid(column=0, row=1, columnspan=2, sticky="nw", pady=50)

user_input_label.grid(column=0, row=2, sticky="sw")
user_input.grid(column=0, row=3, sticky="nsew")
enter_button.grid(column=0, row=4, sticky="nsew")

problem_label.grid(column=0, row=5, sticky="sw")
ProblemSolutionText.grid(column=0, row=6, sticky="nsew")

# Algorithm side (right column)
AlgorithmLabel.grid(column=1, row=2, sticky="sw", padx=20)
Algorithm.grid(column=1, row=3, rowspan=4, sticky="nsew", padx=20)

root.mainloop()