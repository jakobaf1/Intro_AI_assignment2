
from core.formula import *


A = Var("A")
B = Var("B")

formula = And(
    Biconditional(A, B),
    Not(A)
)

print(to_string(formula))