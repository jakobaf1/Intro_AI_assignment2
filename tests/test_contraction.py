from core.formula import *
from revision.belief_base import BeliefBase
from revision.contraction import contract
from entailment.resolution import entails
from revision.expansion import *

p = Var("p")
q = Var("q")
r = Var("r")

# If BB doesn't entail the formula, contraction should change nothing
def contraction_test_vacuity():
    print("=== Test - Vacuity ===")
    bb = BeliefBase()
    bb.add(p, priority=5)
    print(f"Before: {bb.pretty_print_belief_base()}")
    print(f"Contracting with q: B%q")
    result = contract(bb, q)  # BB doesn't entail q
    print(f"After: {result.pretty_print_belief_base()}")
    assert len(result) == 1, f"Expected 1 belief, got {len(result)}"
    assert p in result, "p should still be in the belief base"
    # print("PASSED: Belief base unchanged when formula not entailed\n")

def contraction_test_success():
    # BB = {p}, contract by p → should remove p
    print("=== Test - Success ===")
    bb = BeliefBase()
    bb.add(p)
    bb.add(Imp(p,q))
    print(f"Before: {bb.pretty_print_belief_base()}")
    print(f"Performing B % q")
    result = contract(bb, q)
    print(f"Result: {result.pretty_print_belief_base()}")
    assert not entails(result, p), "BB should no longer entail p"

    # print("PASSED: p successfully contracted\n")

def contraction_test_extensionality():
    print("=== Test - Extensionality ===")
    bb = BeliefBase()
    bb.add(p, priority=0)
    bb.add(Imp(p, q))

    # p and ¬¬p  are logically equivalent
    # print(f"we have q ↔ ¬¬q ∈ Cn(∅) and B = {bb.pretty_print_belief_base()}")
    print(f"Before: {bb.pretty_print_belief_base()}")
    print(f"Extensionality: We must then have B % p = B % ¬¬q")
    print(f"This contraction leads to: {contract(bb,q).pretty_print_belief_base()} = {contract(bb,Not(Not(q))).pretty_print_belief_base()}")

# BB = {p (pri=10), q (pri=1)}, contract by (p & q)
# Both {p} and {q} don't entail (p & q), but {p} has higher priority → keep p
def contraction_test_priority():
    print("=== Test - priority ===")
    bb = BeliefBase()
    bb.add(p, priority=10)
    bb.add(q, priority=1)
    print(f"Before: {bb.pretty_print_belief_base_with_prio()}")
    result = contract(bb, And(p, q))
    print(f"We contract: B % (p & q)")
    print(f"After:  {result.pretty_print_belief_base_with_prio()}")
    assert not entails(result, And(p, q)), "BB should no longer entail p & q"
    assert p in result, "p (higher priority) should be kept"
    # print("PASSED: Higher priority belief kept\n")

def contraction_test_recovery():
    print("=== Test - Recovery ===")
    bb = BeliefBase()
    bb.add(p, priority=0)
    bb.add(Imp(p, q), priority=0)

    contracted_then_expanded = expand(contract(bb, q), q)
    print(f"Before: {bb.pretty_print_belief_base()}")
    print(f"Recovery: B = (B % q) + q")
    print(f"leads to: {bb.pretty_print_belief_base()} = {contracted_then_expanded.pretty_print_belief_base()}")

    for formula in bb:
        assert formula in contracted_then_expanded, \
            f"Recovery violated: {formula_to_string(formula)} lost after (B ÷ q) + q"

# BB = {p, q, p→q}, contract by q
# Should keep as many beliefs as possible while not entailing q
# print("=== Test 3 ===")
# bb = BeliefBase()
# bb.add(p, priority=5)
# bb.add(q, priority=3)
# bb.add(Imp(p, q), priority=7)
# print(f"Before: {bb}")
# result = contract(bb, q)
# print(f"After:  {result}")
# assert not entails(result, q), "BB should no longer entail q"
# print(f"Size: {len(result)} (should keep as many as possible)")
# print("PASSED: Largest non-entailing subset found\n")

# # BB = {p, q, r}, contract by p
# print("=== Test 5 ===")
# bb = BeliefBase()
# bb.add(p, priority=3)
# bb.add(q, priority=5)
# bb.add(r, priority=7)
# print(f"Before: {bb}")
# result = contract(bb, p)
# print(f"After:  {result}")
# assert not entails(result, p), "BB should no longer entail p"
# assert q in result, "q should still be there"
# assert r in result, "r should still be there"
# print("PASSED: Only p removed, q and r kept\n")

# print("ALL TESTS PASSED!")
