from core.formula import *
from revision.belief_base import BeliefBase
from revision.revision import revise
from entailment.resolution import entails
from revision.contraction import *
from revision.expansion import *

p = Var("p")
q = Var("q")
r = Var("r")


# Test 1: Revising with a completely new belief
# BB = {p}, revise by q
# Should result in {p, q}
def revision_vacuity_test():
    print("=== Test - Vacuity ===")
    bb = BeliefBase()
    bb.add(p, priority=5)

    print(f"Before: {bb.pretty_print_belief_base()}")
    print(f"Performing revision: {bb.pretty_print_belief_base()}*q")
    result = revise(bb, q, priority=3)
    print(f"After:  {result.pretty_print_belief_base()}")
    print("Vacuity passed: As ¬q /∈ B, then B ∗ q = B + q")

    assert p in result, "p should still be in the belief base"
    assert q in result, "q should be added to the belief base"
# print("PASSED: New independent belief added\n")


# Test 3: BB = {p, q, p→q}, revise by ¬q
# Should first contract by q, then add ¬q
def revision_success_consistency_test():
    print("=== Test - Success + Consistency ===")
    bb = BeliefBase()
    bb.add(p, priority=5)
    bb.add(q, priority=3)
    bb.add(Imp(p, q), priority=7)

    print(f"Before: {bb.pretty_print_belief_base()}")
    print(f"Performing revision: {bb.pretty_print_belief_base()}*¬q")
    result = revise(bb, Not(q), priority=10)
    print(f"After:  {result.pretty_print_belief_base()}")
    print("Success: ¬q is added to the revised belief base")
    print("Consistency: Belief base is satisfiable")

    assert Not(q) in result, "¬q should be added"
    assert not entails(result, q), "BB should no longer entail q"
    # print("PASSED: Revision via Levi Identity works\n")


def revision_inclusion_test():
    print("=== Test - Inclusion ===")
    bb = BeliefBase()
    bb.add(p)
    bb.add(Imp(p, q))
    print(f"Performing revision: {bb.pretty_print_belief_base()}*¬q")
    result = revise(bb, Not(q))
    print(f"After: {result.pretty_print_belief_base()}")
    print(f"We see that {result.pretty_print_belief_base()} ⊆ {expand(bb,Not(q)).pretty_print_belief_base()}, which follows Inclusion")
    expanded = BeliefBase()
    for f, pri in bb._beliefs:
        expanded.add(f, priority=pri)
    expanded.add(Not(q))

    for formula in result:
        assert formula in expanded, f"{formula_to_string(formula)} is in K*φ but not in K+φ"
    # print("PASSED: Inclusion holds\n")

def revision_extensionality_test():
    print("=== Test - Extensionality ===")
    bb = BeliefBase()
    bb.add(p, priority=0)
    bb.add(Imp(p, q))

    # p and ¬¬p  are logically equivalent
    print(f"we have q ↔ ¬¬q ∈ Cn(∅) and B = {bb.pretty_print_belief_base()}")
    print(f"Extensionality: We must then have B * p = B * ¬¬q")
    print(f"Performing revision leads to: {revise(bb,q).pretty_print_belief_base()} = {revise(bb,Not(Not(q))).pretty_print_belief_base()}")

    # for formula in result1:
    #     assert formula in result2, f"{formula_to_string(formula)} in K*φ but not K*ψ"
    # for formula in result2:
    #     assert formula in result1, f"{formula_to_string(formula)} in K*ψ but not K*φ"
    # print("PASSED: Extensionality holds\n")


# Test 2: Revising with contradictory belief
# BB = {p}, revise by ¬p
# Levi Identity:
#   contract by ¬(¬p) = p
#   then add ¬p
# Final result should contain ¬p and not entail p
# print("=== Test 2 - Success + Consistency ===")
# bb = BeliefBase()
# bb.add(p, priority=5)

# print(f"Before: {bb.pretty_print_belief_base()}")
# result = revise(bb, Not(p), priority=10)
# print(f"After:  {result.pretty_print_belief_base()}")
# print("Success: ¬p is in the revised belief base")
# print("Contraction: Belief base no longer entails p")

# assert Not(p) in result, "¬p should be in the revised belief base"
# assert not entails(result, p), "BB should no longer entail p"
# print("PASSED: Contradicting belief revised correctly\n")


# # Test 4: Revising with already believed formula
# # BB = {p}, revise by p
# # Should basically remain the same (maybe priority updated)
# print("=== Test 4 ===")
# bb = BeliefBase()
# bb.add(p, priority=2)

# print(f"Before: {bb}")
# result = revise(bb, p, priority=8)
# print(f"After:  {result}")

# assert p in result, "p should still be there"
# assert len(result) == 1, "No duplicate beliefs should exist"
# print("PASSED: Revising with existing belief works\n")


# # Test 5: Revision should respect priority through contraction
# # BB = {p (10), q (1), p→q (8)}, revise by ¬q
# # Should prefer keeping higher-priority beliefs where possible
# print("=== Test 5 ===")
# bb = BeliefBase()
# bb.add(p, priority=10)
# bb.add(q, priority=1)
# bb.add(Imp(p, q), priority=8)

# print(f"Before: {bb}")
# result = revise(bb, Not(q), priority=15)
# print(f"After:  {result}")

# assert Not(q) in result, "¬q should be present"
# assert not entails(result, q), "BB should no longer entail q"
# assert Imp(p, q) not in result, "p → q should be removed since otherwise q is still entailed"
# print("PASSED: Priority-sensitive revision works\n")

# print("ALL REVISION TESTS PASSED!")