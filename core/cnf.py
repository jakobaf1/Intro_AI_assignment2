from core.formula import *

def eliminate_biconditional(f: Formula):
    # p ↔ q  →  (p → q) ∧ (q → p)
    if isinstance(f, Iff):
        return And(Imp(eliminate_biconditional(f.left), eliminate_biconditional(f.right)),
                    Imp(eliminate_biconditional(f.right), eliminate_biconditional(f.left)))
    if isinstance(f, And):
        return And(eliminate_biconditional(f.left), eliminate_biconditional(f.right))
    if isinstance(f, Or):
        return Or(eliminate_biconditional(f.left), eliminate_biconditional(f.right))
    if isinstance(f, Imp):
        return Imp(eliminate_biconditional(f.left), eliminate_biconditional(f.right))
    if isinstance(f, Not):
        return Not(eliminate_biconditional(f.operand))
    return f

def eliminate_implication(f: Formula):
    # p → q  →  ¬p ∨ q
    if isinstance(f, Imp):
        return Or(Not(eliminate_implication(f.left)), eliminate_implication(f.right))
    if isinstance(f, And):
        return And(eliminate_implication(f.left), eliminate_implication(f.right))
    if isinstance(f, Or):
        return Or(eliminate_implication(f.left), eliminate_implication(f.right))
    if isinstance(f, Not):
        return Not(eliminate_implication(f.operand))
    return f

def move_negation_inward(f: Formula):
    # ¬(p ∨ q)  →  ¬p ∧ ¬q
    # ¬(p ∧ q)  →  ¬p ∨ ¬q
    # ¬(¬p)     →  p
    if isinstance(f, Not):
        if isinstance(f.operand, Not):
            return move_negation_inward(f.operand.operand)
        if isinstance(f.operand, And):
            return Or(move_negation_inward(Not(f.operand.left)), 
                      move_negation_inward(Not(f.operand.right)))
        if isinstance(f.operand, Or):
            return And(move_negation_inward(Not(f.operand.left)), 
                       move_negation_inward(Not(f.operand.right)))
        return f
    if isinstance(f, And):
        return And(move_negation_inward(f.left), move_negation_inward(f.right))
    if isinstance(f, Or):
        return Or(move_negation_inward(f.left), move_negation_inward(f.right))
    return f

def distribute_and_over_or(f: Formula):
    # (p ∧ q) ∨ r → (p ∨ r) ∧ (q ∨ r)
    # p ∨ (q ∧ r) → (p ∨ q) ∧ (p ∨ r)
    if isinstance(f, Or):
        if isinstance(f.left, And):
            result = And(Or(distribute_and_over_or(f.left.left), distribute_and_over_or(f.right)),
                       Or(distribute_and_over_or(f.left.right), distribute_and_over_or(f.right)))
            return distribute_and_over_or(result)
        if isinstance(f.right, And):
            result = And(Or(distribute_and_over_or(f.left), distribute_and_over_or(f.right.left)),
                       Or(distribute_and_over_or(f.left), distribute_and_over_or(f.right.right)))
            return distribute_and_over_or(result)
    if isinstance(f, And):
        return And(distribute_and_over_or(f.left), distribute_and_over_or(f.right))
    if isinstance(f, Not):
        return Not(distribute_and_over_or(f.operand))
    return f


def to_cnf(f: Formula):
    f = eliminate_biconditional(f)
    f = eliminate_implication(f)
    f = move_negation_inward(f)
    f = distribute_and_over_or(f)
    return f
