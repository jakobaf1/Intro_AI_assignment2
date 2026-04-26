from core.formula import *
from core.cnf import to_cnf

def extract_literals(f: Formula):
    # Splitter en klausul op i et sæt af literals
    if isinstance(f, Or):
        return extract_literals(f.left) | extract_literals(f.right)
    return {f}

def extract_singles(f: Formula):
    # Splitter 1 CNF-formel op i en liste af klausuler
    if isinstance(f, And):
        return extract_singles(f.left) + extract_singles(f.right)
    return [extract_literals(f)]

def extract_clauses(formulas):
    # Splitter en liste af CNF-formler op i en liste ad klausul-sæt
    clauses = []
    for f in formulas:
        clauses += extract_singles(f)
    return clauses

def resolve(clause1, clause2):
    # Resolves 2 klausulsæt ved at tjekke om en literal og den negerede optræder i to sæt
    for literal in clause1:
        if Not(literal) in clause2:
            new_clause = (clause1 - {literal}) | (clause2 - {Not(literal)})
            return new_clause
        if isinstance(literal, Not) and literal.operand in clause2:
            new_clause = (clause1 - {literal}) | (clause2 - {literal.operand})
            return new_clause
    return None

def resolution(clauses):
    # Resolves alle klausulsæt parvist (tjekker om der opstår tom klausul og dermed modstrid)
    while True:
        new = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvent = resolve(clauses[i], clauses[j])
                if resolvent is None:
                    continue
                if resolvent == set(): # Hvis der er opstået en tom klausul
                    return True
                if resolvent not in clauses:
                    new.append(resolvent)
        if not new:
            return False # Ingen nye clauses og ingen tomme clauses
        clauses += new


