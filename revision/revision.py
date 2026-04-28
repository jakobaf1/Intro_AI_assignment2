from revision.belief_base import BeliefBase
from revision.contraction import contract
from revision.expansion import expand
from core.formula import Not

def revise(belief_base: BeliefBase, formula, priority: int = 0) -> BeliefBase:
    # AGM Revision using the Levi Identity:
    # B * φ := (B ÷ ¬φ) + φ

    # "Belief revision can be defined as first removing any inconsistency with the incoming information and then adding the information itself."

    # Step 1: Contract by Not(φ)
    neg_formula = Not(formula)
    contracted_bb = contract(belief_base, neg_formula)

    # Step 2: Expand with φ
    revised_bb = expand(contracted_bb, formula, priority)

    return revised_bb