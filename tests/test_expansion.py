from core.formula import *
from revision.belief_base import BeliefBase
from revision.expansion import expand
from entailment.resolution import entails

p = Var("p")
q = Var("q")
r = Var("r")


# BB = {}, expand by p
print("=== Test 1 ===")
bb = BeliefBase()
result = expand(bb, p, priority=5)

assert len(result) == 1, f"Expected 1 belief, got {len(result)}"
assert p in result, "p should be added to the belief base"

print(f"Result: {result}")
print("PASSED: p successfully added to empty belief base\n")


# BB = {p}, expand by q
print("=== Test 2 ===")
bb = BeliefBase()
bb.add(p, priority=5)

result = expand(bb, q, priority=3)

assert len(result) == 2, f"Expected 2 beliefs, got {len(result)}"
assert p in result, "p should still be in the belief base"
assert q in result, "q should be added to the belief base"

print(f"Result: {result}")
print("PASSED: q added while keeping existing beliefs\n")


# BB = {p}, expand by ¬p
# Expansion allows inconsistency
print("=== Test 3 ===")
bb = BeliefBase()
bb.add(p, priority=5)

result = expand(bb, Not(p), priority=4)

assert p in result, "p should still be present"
assert Not(p) in result, "¬p should be added"
assert entails(result, p), "BB should still entail p"

print(f"Result: {result}")
print("PASSED: Expansion allows inconsistent beliefs\n")


# BB = {p}, expand by p again with new priority
# Should update priority, not duplicate
print("=== Test 4 ===")
bb = BeliefBase()
bb.add(p, priority=2)

result = expand(bb, p, priority=10)

assert len(result) == 1, f"Expected 1 belief, got {len(result)}"
assert result.get_priority(p) == 10, "Priority of p should be updated to 10"

print(f"Result: {result}")
print("PASSED: Existing belief priority updated\n")


# BB = {p, q}, expand by (p → r)
print("=== Test 5 ===")
bb = BeliefBase()
bb.add(p, priority=5)
bb.add(q, priority=4)

formula = Imp(p, r)
result = expand(bb, formula, priority=7)

assert p in result, "p should still be present"
assert q in result, "q should still be present"
assert formula in result, "p → r should be added"

print(f"Result: {result}")
print("PASSED: Complex formula added successfully\n")


print("ALL EXPANSION TESTS PASSED!")