from core.formula import *
from core.cnf import *
from utils.parser import *

print("Enter formulas to update the belief base. If finished, enter an empty string to end the program")
while True:
    formula_str = input("Enter formula: ")

    # Exit
    if formula_str == "":
        break
    
    # Parse input from str to Formula
    formula = parse_formula(formula_str)
    print(f"translated {to_string(formula)} into: {formula}")
    
    # converting to CNF:
    cnf = to_cnf(formula)
    print(f"CNF format: {to_string(cnf)}")

    
