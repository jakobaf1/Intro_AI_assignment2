from revision.belief_base import *

# test for at se om belief base virker. Har ikke logical entailment
if __name__ == "__main__":
 
    bb = BeliefBase()
 
    p = Var("p")
    q = Var("q")
    r = Var("r")
 
    bb.add(Imp(p, q), priority=10) 
    bb.add(p, priority=5)           
    bb.add(Not(r), priority=1)    
 
    print(bb)
    print()
    print(f"Antal overbevisninger: {len(bb)}")
    print(f"Indeholder p: {p in bb}")
    print(f"Indeholder q: {q in bb}")
    print()
    print("Iteration (højest prioritet først):")
    for f in bb:
        print(f"  {to_string(f)}")
    print()
 
    # Test fjernelse
    bb.remove(p)
    print("Efter fjernelse af p:")
    print(bb)