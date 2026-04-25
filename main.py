from core.formula import *
from utils.parser import *

print("Enter formulas to update the belief base. If finished, enter an empty string to end the program")
while True:
    formula_str = input("Enter formula: ")
    if formula_str == "":
        break
    ast = parse_formula(formula_str)
    print(ast)