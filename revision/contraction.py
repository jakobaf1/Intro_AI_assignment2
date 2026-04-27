from revision.belief_base import BeliefBase
from entailment.resolution import entails
from itertools import combinations

def contract(belief_base: BeliefBase, formula) -> BeliefBase:
    """
    Find the LARGEST subset of the belief base that does NOT entail the formula.
    """
    # Vacuity: if the belief base doesn't entail the formula, nothing to do
    if not entails(belief_base, formula):
        return belief_base

    # Tautologies can't be contracted
    if formula == True:
        return belief_base
    
    all_beliefs = list(belief_base._beliefs)  
    n = len(all_beliefs)
    
    # Try removing the fewest beliefs possible
    for num_to_remove in range(1, n + 1):
        best_subset = None
        best_priority = -1
        
        # Try all combinations of beliefs to remove
        for to_remove in combinations(all_beliefs, num_to_remove):
            temp_bb = BeliefBase()
            for f, p in all_beliefs:
                if (f, p) not in to_remove:
                    temp_bb.add(f, p)
            
            # Check if this subset no longer entails the formula
            if not entails(temp_bb, formula):
                kept_priority = sum(p for _, p in all_beliefs if (_, p) not in to_remove)
                if kept_priority > best_priority:
                    best_priority = kept_priority
                    best_subset = temp_bb
        
        # If we found a valid subset at this removal size, return it
        if best_subset is not None:
            return best_subset
    
    # Fallback: return empty belief base
    return BeliefBase()
