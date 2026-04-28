from core.formula import *
from revision.belief_base import BeliefBase
from revision.revision import revise
from entailment.resolution import entails

p = Var("p")
q = Var("q")
r = Var("r")


# Test 1: Revising with a completely new belief
# BB = {p}, revise by q
# Should result in {p, q}
print("=== Test 1 ===")
bb = BeliefBase()
bb.add(p, priority=5)

print(f"Before: {bb}")
result = revise(bb, q, priority=3)
print(f"After:  {result}")

assert p in result, "p should still be in the belief base"
assert q in result, "q should be added to the belief base"
print("PASSED: New independent belief added\n")


# Test 2: Revising with contradictory belief
# BB = {p}, revise by ¬p
# Levi Identity:
#   contract by ¬(¬p) = p
#   then add ¬p
# Final result should contain ¬p and not entail p
print("=== Test 2 ===")
bb = BeliefBase()
bb.add(p, priority=5)

print(f"Before: {bb}")
result = revise(bb, Not(p), priority=10)
print(f"After:  {result}")

assert Not(p) in result, "¬p should be in the revised belief base"
assert not entails(result, p), "BB should no longer entail p"
print("PASSED: Contradicting belief revised correctly\n")


# Test 3: BB = {p, q, p→q}, revise by ¬q
# Should first contract by q, then add ¬q
print("=== Test 3 ===")
bb = BeliefBase()
bb.add(p, priority=5)
bb.add(q, priority=3)
bb.add(Imp(p, q), priority=7)

print(f"Before: {bb}")
result = revise(bb, Not(q), priority=10)
print(f"After:  {result}")

assert Not(q) in result, "¬q should be added"
assert not entails(result, q), "BB should no longer entail q"
print("PASSED: Revision via Levi Identity works\n")


# Test 4: Revising with already believed formula
# BB = {p}, revise by p
# Should basically remain the same (maybe priority updated)
print("=== Test 4 ===")
bb = BeliefBase()
bb.add(p, priority=2)

print(f"Before: {bb}")
result = revise(bb, p, priority=8)
print(f"After:  {result}")

assert p in result, "p should still be there"
assert len(result) == 1, "No duplicate beliefs should exist"
print("PASSED: Revising with existing belief works\n")


# Test 5: Revision should respect priority through contraction
# BB = {p (10), q (1), p→q (8)}, revise by ¬q
# Should prefer keeping higher-priority beliefs where possible
print("=== Test 5 ===")
bb = BeliefBase()
bb.add(p, priority=10)
bb.add(q, priority=1)
bb.add(Imp(p, q), priority=8)

print(f"Before: {bb}")
result = revise(bb, Not(q), priority=15)
print(f"After:  {result}")

assert Not(q) in result, "¬q should be present"
assert not entails(result, q), "BB should no longer entail q"
assert Imp(p, q) not in result, "p → q should be removed since otherwise q is still entailed"
print("PASSED: Priority-sensitive revision works\n")


print("ALL REVISION TESTS PASSED!")