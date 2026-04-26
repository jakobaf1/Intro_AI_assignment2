from core.formula import *
from core.cnf import to_cnf
from entailment.resolution import *

p = Var("p")
q = Var("q")
r = Var("r")

# Test extract_literals
# ¬r ∨ p  →  {¬r, p}
clause = Or(Not(r), p)
assert extract_literals(clause) == {Not(r), p}, "extract_literals fejlede"
print("extract_literals OK")
print({to_string(f) for f in extract_literals(clause)})

# Test extract_singles
# (¬r ∨ p) ∧ (¬p ∨ q)  →  [{¬r, p}, {¬p, q}]
cnf = And(Or(Not(r), p), Or(Not(p), q))
assert extract_singles(cnf) == [{Not(r), p}, {Not(p), q}], "extract_singles fejlede"
print("extract_singles OK")

# Test extract_clauses med to formler
# p → q  og  p  skal give [{¬p, q}, {p}]
formulas = [to_cnf(Imp(p, q)), to_cnf(p)]
clauses = extract_clauses(formulas)
assert {Not(p), q} in clauses, "extract_clauses fejlede på p→q"
assert {p} in clauses, "extract_clauses fejlede på p"
print("extract_clauses OK")


# Entailment: {p→q, p} ⊨ q
# Bevis: tilføj ¬q og vis modstrid

p = Var("p")
q = Var("q")

# p→q bliver ¬p∨q, p bliver {p}, ¬q bliver {¬q}
clauses = [
    {Not(p), q},  # ¬p ∨ q  (fra p→q)
    {p},          # p
    {Not(q)}      # ¬q  (negationen af det vi vil bevise)
]

result = resolution(clauses)
assert result == True, "Resolution fejlede"
print(f"Resolution OK: {result}")