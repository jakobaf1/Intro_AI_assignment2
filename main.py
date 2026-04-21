from core.formula import *

A = Var("A")
B = Var("B")

formula = And(
    Iff(A, B),
    Not(A)
)

print(to_string(formula))