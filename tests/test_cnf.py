from core.cnf import *

# p → q  skal blive  ¬p ∨ q
print(to_string(to_cnf(Imp(Var("p"), Var("q")))))

# ¬(p ∧ q)  skal blive  ¬p ∨ ¬q
print(to_string(to_cnf(Not(And(Var("p"), Var("q"))))))

print(to_string(to_cnf(Iff(Var("r"), (Or(Var("p"), Var("s")))))))