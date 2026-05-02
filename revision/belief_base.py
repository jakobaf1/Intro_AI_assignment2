from core.formula import *

class BeliefBase:
    """
    Gemmer Beliefs som tupler (formel, prioritet). Højere prioritering -> vigtigere
    """

    def __init__(self):
        self._beliefs: list[tuple[Formula, int]] = []

    def add(self, formula: Formula, priority: int = 0):
        # Tjekker om formel allerede er i belief base og opdatere prioritet hvis den er
        for i, (f, p) in enumerate(self._beliefs):
            if f == formula:
                self._beliefs[i] = (formula, priority)
                return
        self._beliefs.append((formula, priority))

    def remove(self, formula: Formula):
        self._beliefs = [(f, p) for f, p in self._beliefs if f != formula]

    def get_formulas(self):
        # Sorterer listen af formler i belief base efter prioritet
        sorted_beliefs = sorted(self._beliefs, key=lambda x: x[1], reverse=True)
        return [f for f, p in sorted_beliefs]
    
    def get_priority(self, formula: Formula):
        for f, p in self._beliefs:
            if f == formula:
                return p
        return None
    
    def pretty_print_belief_base(self):
        formulas = self.get_formulas()
        str = "{"
        for i in range(len(formulas)):
            str += f"{formula_to_string(formulas[i])}"
            if i != len(formulas)-1:
                str += ", "
        str += "}"
        return str
    
    def __contains__(self, formula: Formula) -> bool:
        return any(f == formula for f, _ in self._beliefs)
 
    def __iter__(self):
        return iter(self.get_formulas())
 
    def __len__(self) -> int:
        return len(self._beliefs)
 
    def __str__(self) -> str:
        if not self._beliefs:
            return "BeliefBase { tom }"
        sorted_beliefs = sorted(self._beliefs, key=lambda x: x[1], reverse=True)
        lines = [f"  [{p}] {formula_to_string(f)}" for f, p in sorted_beliefs]
        return "BeliefBase {\n" + "\n".join(lines) + "\n}"
 
    def __repr__(self) -> str:
        return self.__str__()