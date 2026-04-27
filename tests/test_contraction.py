from core.formula import *
from revision.belief_base import BeliefBase
from revision.contraction import contract
from entailment.resolution import entails

p = Var("p")
q = Var("q")
r = Var("r")

# If BB doesn't entail the formula, contraction should change nothing
print("=== Test 1 ===")
bb = BeliefBase()
bb.add(p, priority=5)
result = contract(bb, q)  # BB doesn't entail q
assert len(result) == 1, f"Expected 1 belief, got {len(result)}"
assert p in result, "p should still be in the belief base"
print("PASSED: Belief base unchanged when formula not entailed\n")

# BB = {p}, contract by p → should remove p
print("=== Test 2 ===")
bb = BeliefBase()
bb.add(p, priority=5)
result = contract(bb, p)
assert not entails(result, p), "BB should no longer entail p"
print(f"Result: {result}")
print("PASSED: p successfully contracted\n")

# BB = {p, q, p→q}, contract by q
# Should keep as many beliefs as possible while not entailing q
print("=== Test 3 ===")
bb = BeliefBase()
bb.add(p, priority=5)
bb.add(q, priority=3)
bb.add(Imp(p, q), priority=7)
print(f"Before: {bb}")
result = contract(bb, q)
print(f"After:  {result}")
assert not entails(result, q), "BB should no longer entail q"
print(f"Size: {len(result)} (should keep as many as possible)")
print("PASSED: Largest non-entailing subset found\n")

# BB = {p (pri=10), q (pri=1)}, contract by (p & q)
# Both {p} and {q} don't entail (p & q), but {p} has higher priority → keep p
print("=== Test 4 ===")
bb = BeliefBase()
bb.add(p, priority=10)
bb.add(q, priority=1)
print(f"Before: {bb}")
result = contract(bb, And(p, q))
print(f"After:  {result}")
assert not entails(result, And(p, q)), "BB should no longer entail p & q"
assert p in result, "p (higher priority) should be kept"
print("PASSED: Higher priority belief kept\n")

# BB = {p, q, r}, contract by p
print("=== Test 5 ===")
bb = BeliefBase()
bb.add(p, priority=3)
bb.add(q, priority=5)
bb.add(r, priority=7)
print(f"Before: {bb}")
result = contract(bb, p)
print(f"After:  {result}")
assert not entails(result, p), "BB should no longer entail p"
assert q in result, "q should still be there"
assert r in result, "r should still be there"
print("PASSED: Only p removed, q and r kept\n")

print("ALL TESTS PASSED!")
