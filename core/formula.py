from dataclasses import dataclass

# Base class
class Formula:
    pass


@dataclass(frozen=True)
class Var(Formula):
    name: str


@dataclass(frozen=True)
class Not(Formula):
    operand: Formula


@dataclass(frozen=True)
class And(Formula):
    left: Formula
    right: Formula


@dataclass(frozen=True)
class Or(Formula):
    left: Formula
    right: Formula


@dataclass(frozen=True)
class Implies(Formula):
    left: Formula
    right: Formula

@dataclass(frozen=True)
class Biconditional(Formula):
    left: Formula
    right: Formula

def to_string(f):
    if isinstance(f, Var):
        return f.name
    if isinstance(f, Not):
        return f"¬{to_string(f.operand)}"
    if isinstance(f, And):
        return f"({to_string(f.left)} ∧ {to_string(f.right)})"
    if isinstance(f, Or):
        return f"({to_string(f.left)} ∨ {to_string(f.right)})"
    if isinstance(f, Implies):
        return f"({to_string(f.left)} → {to_string(f.right)})"
    if isinstance(f, Biconditional):
        return f"({to_string(f.left)} ↔ {to_string(f.right)})"