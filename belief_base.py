from ast_types import Formula, Var, Not, And, Or, Implies, Biconditional, to_string

A = Var("A")
B = Var("B")

formula = And(
    Biconditional(A, B),
    Not(A)
)

print(to_string(formula))