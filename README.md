# Belief Revision Engine
### 02180 Introduction to AI — Assignment 2

A propositional logic belief revision engine implementing the AGM framework, including a parser, CNF converter, resolution-based entailment checker, and contraction/expansion/revision operators.

---

## Project Structure

```
.
├── core/
│   ├── formula.py          # Formula dataclasses (Var, Not, And, Or, Imp, Iff)
│   └── cnf.py              # CNF conversion
├── utils/
│   └── parser.py           # Lexer + recursive descent parser
├── entailment/
│   └── resolution.py       # Resolution-based entailment checker
├── revision/
│   ├── belief_base.py      # BeliefBase data structure
│   ├── contraction.py      # Maxi-choice contraction
│   ├── expansion.py        # Expansion operator
│   └── revision.py         # Revision via Levi identity
├── tests/
│   ├── test_revision.py    # AGM postulate tests for revision
│   └── test_contraction.py # AGM postulate tests for contraction
└── main.py
```

---

## Running the Engine

```bash
python main.py
```

On startup, the engine initialises an empty belief base and waits for input.

---

## Usage

### Adding a formula to the belief base

Type a propositional formula to add it to the belief base. Optionally assign a priority (integer) by appending it after a comma. If no priority is given, it defaults to `0`.

```
> p -> q
> p -> q, 5
```

Higher priority beliefs are preserved over lower priority ones during contraction.

The engine automatically determines whether to **expand** or **revise**:
- If the formula is already entailed by the belief base → **expand**
- Otherwise → **revise** via the Levi identity: `B * φ = (B ÷ ¬φ) + φ`

### Supported syntax

| Connective      | Symbols          |
|-----------------|------------------|
| Negation        | `~` or '-' or `¬`|
| Conjunction     | `&` or `∧`       |
| Disjunction     | `|` or `∨`       |
| Implication     | `->` or `→`      |
| Biconditional   | `<->` or `↔`     |
| Parentheses     | `(` `)`          |

Example formulas:
```
> p
> ~p
> p -> q, 10 (gives priority 10)
> (p | q) & ~r, 3 (gives priority 3)
> p <-> q
```

### Exiting

Press `Ctrl+C` to exit the program.

---

## Running Tests

Tests are triggered by typing a number at the prompt:

| Input | Test |
|-------|------|
| `1`   | Revision — Success + Consistency |
| `2`   | Revision — Vacuity |
| `3`   | Revision — Inclusion |
| `4`   | Revision — Extensionality |
| `5`   | Contraction — Vacuity |
| `6`   | Contraction — Success |
| `7`   | Contraction — Priority |
| `8`   | Contraction — Extensionality |
| `9`   | Contraction — Recovery |


## Implementation Notes

**Contraction** uses maxi-choice with priority-based selection. Among all minimal removals that break entailment of `φ`, the subset maximising the sum of retained priorities is chosen. Ties are broken by insertion order.

**Recovery** is knowingly violated as a consequence of maxi-choice contraction. This is a deliberate design tradeoff — maxi-choice prioritises minimal change over reversibility. See the report for a full discussion.

**Revision** is implemented via the Levi identity: contract the negation of the new formula, then expand with it.