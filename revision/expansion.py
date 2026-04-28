from revision.belief_base import BeliefBase

def expand(belief_base: BeliefBase, formula, priority: int = 0) -> BeliefBase:
    # Expansion: B + ϕ; ϕ is added to B giving a new belief set B'.

    # Create copy so we don't mutate the original
    new_bb = BeliefBase()

    for f, p in belief_base._beliefs:
        new_bb.add(f, p)

    new_bb.add(formula, priority)

    return new_bb