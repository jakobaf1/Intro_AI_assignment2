from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Optional

from core.formula import *


# First we define the types of tokens we can get
class TokenType(Enum):
    # Atoms & constants
    ATOM    = auto()   # e.g. p, q, r
    TRUE    = auto()   # True
    FALSE   = auto()   # False
    # Connectives
    NOT     = auto()    # -
    AND     = auto()    # &  or  ∧
    OR      = auto()    # |  or  ∨
    IMP = auto()        # ->
    IFF  = auto()       # <->
    # Grouping
    LPAREN  = auto()   # (
    RPAREN  = auto()   # )
    # Control
    EOF     = auto()


@dataclass
class Token:
    type:  TokenType
    value: str = ""

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})" if self.value else f"Token({self.type.name})"


class LexerError(Exception):
    pass

# Now we make a Lexer which turns strings into tokens
class Lexer:
    # Map multi-char symbolic operators to token types
    SYMBOLS = {
        "<->": TokenType.IFF,
        "->":  TokenType.IMP,
        "-":   TokenType.NOT,
        "~":   TokenType.NOT,
        "¬":   TokenType.NOT,
        "&":   TokenType.AND,
        "∧":   TokenType.AND,
        "|":   TokenType.OR,
        "∨":   TokenType.OR,
        "→":   TokenType.IMP,
        "↔":   TokenType.IFF,
        "(":   TokenType.LPAREN,
        ")":   TokenType.RPAREN,
    }

    def __init__(self, text: str):
        self.text = text
        self.pos  = 0

    def _peek(self, length=1) -> str:
        return self.text[self.pos : self.pos + length]

    def _advance(self, length=1):
        self.pos += length

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.pos < len(self.text):
            # skip whitespace
            if self.text[self.pos].isspace():
                self._advance()
                continue

            matched = False
            for symbol, ttype in self.SYMBOLS.items():
                if self.text[self.pos:].startswith(symbol):
                    tokens.append(Token(ttype))
                    self._advance(len(symbol))
                    matched = True
                    break
            if matched:
                continue

            if self.text[self.pos].isalpha() or self.text[self.pos] == "_":
                start = self.pos
                while self.pos < len(self.text) and (
                    self.text[self.pos].isalnum() or self.text[self.pos] == "_"
                ):
                    self._advance()
                word = self.text[start : self.pos]
                if word in ("True", "true"):
                    tokens.append(Token(TokenType.TRUE))
                elif word in ("False", "false"):
                    tokens.append(Token(TokenType.FALSE))
                else:
                    tokens.append(Token(TokenType.ATOM, word))
                continue

            raise LexerError(f"Unexpected character {self.text[self.pos]!r} at position {self.pos}")

        tokens.append(Token(TokenType.EOF))
        return tokens
    
# Representation of the nodes in the AST tree
class NodeType(Enum):
    ATOM    = auto()
    TRUE    = auto()
    FALSE   = auto()
    NOT     = auto()
    AND     = auto()
    OR      = auto()
    IMP     = auto()
    IFF     = auto()


# A snigle node in the AST tree
@dataclass
class Node:
    type:  NodeType
    name:  Optional[str]  = None
    left:  Optional["Node"] = field(default=None, repr=False)
    right: Optional["Node"] = field(default=None, repr=False)

    def __str__(self) -> str:
        INFIX = {
            NodeType.AND: "&",
            NodeType.OR: "|",
            NodeType.IMP: "->",
            NodeType.IFF: "<->",
        }
        if self.type == NodeType.ATOM:
            return self.name
        if self.type == NodeType.TRUE:
            return "True"
        if self.type == NodeType.FALSE:
            return "False"
        if self.type == NodeType.NOT:
            child_str = str(self.left)
            # Add parens around compound children for clarity
            if self.left.type not in (NodeType.ATOM, NodeType.TRUE, NodeType.FALSE):
                child_str = f"({child_str})"
            return f"~{child_str}"
        # Binary operators
        op  = INFIX[self.type]
        lhs = str(self.left)
        rhs = str(self.right)
        if self.left.type  not in (NodeType.ATOM, NodeType.TRUE, NodeType.FALSE, NodeType.NOT):
            lhs = f"({lhs})"
        if self.right.type not in (NodeType.ATOM, NodeType.TRUE, NodeType.FALSE, NodeType.NOT):
            rhs = f"({rhs})"
        return f"{lhs} {op} {rhs}"

    def atoms(self) -> set[str]:
        if self.type == NodeType.ATOM:
            return {self.name}
        result = set()
        if self.left:
            result |= self.left.atoms()
        if self.right:
            result |= self.right.atoms()
        return result

    def evaluate(self, model: dict[str, bool]) -> bool:
        match self.type:
            case NodeType.ATOM:
                return model[self.name]
            case NodeType.TRUE:
                return True
            case NodeType.FALSE:
                return False
            case NodeType.NOT:
                return not self.left.evaluate(model)
            case NodeType.AND:
                return self.left.evaluate(model) and self.right.evaluate(model)
            case NodeType.OR:
                return self.left.evaluate(model) or self.right.evaluate(model)
            case NodeType.IMP:
                return (not self.left.evaluate(model)) or self.right.evaluate(model)
            case NodeType.IFF:
                return self.left.evaluate(model) == self.right.evaluate(model)


# Here comes the parser
class ParseError(Exception):
    pass

# the parser is recursively going through the AST tree to decode the input with proper precedence
class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos    = 0

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _consume(self, expected: Optional[TokenType] = None) -> Token:
        tok = self.tokens[self.pos]
        if expected is not None and tok.type != expected:
            raise ParseError(f"Expected {expected.name}, got {tok.type.name}")
        self.pos += 1
        return tok

    def _match(self, *types: TokenType) -> bool:
        return self._peek().type in types

    def parse(self) -> Node:
        node = self._iff()
        self._consume(TokenType.EOF)
        return node

    def _iff(self) -> Node:
        left = self._imp()
        if self._match(TokenType.IFF):
            self._consume()
            right = self._iff()
            return Node(NodeType.IFF, left=left, right=right)
        return left

    def _imp(self) -> Node:
        left = self._or()
        if self._match(TokenType.IMP):
            self._consume()
            right = self._imp()
            return Node(NodeType.IMP, left=left, right=right)
        return left

    def _or(self) -> Node:
        left = self._and()
        while self._match(TokenType.OR):
            self._consume()
            right = self._and()
            left = Node(NodeType.OR, left=left, right=right)
        return left

    def _and(self) -> Node:
        left = self._not()
        while self._match(TokenType.AND):
            self._consume()
            right = self._not()
            left = Node(NodeType.AND, left=left, right=right)
        return left

    def _not(self) -> Node:
        if self._match(TokenType.NOT):
            self._consume()
            operand = self._not()      
            return Node(NodeType.NOT, left=operand)
        return self._primary()

    def _primary(self) -> Node:
        tok = self._peek()

        if tok.type == TokenType.ATOM:
            self._consume()
            return Node(NodeType.ATOM, name=tok.value)

        if tok.type == TokenType.TRUE:
            self._consume()
            return Node(NodeType.TRUE)

        if tok.type == TokenType.FALSE:
            self._consume()
            return Node(NodeType.FALSE)

        if tok.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            node = self._iff()       
            self._consume(TokenType.RPAREN)
            return node

        raise ParseError(f"Unexpected token {tok.type.name} ({tok.value!r}) at position {self.pos}")

# call to parse a given formula.
# Calls upon the lexer to tokenize and then parses the input
def parse_formula(text: str) -> Node:
    tokens = Lexer(text).tokenize()
    node = Parser(tokens).parse()
    return node_to_formula(node)     # Node → Formula

def ast_to_prefix(node: Node) -> str:
    match node.type:
        case NodeType.ATOM:
            return node.name
        case NodeType.TRUE:
            return "TRUE"
        case NodeType.FALSE:
            return "FALSE"
        case NodeType.NOT:
            return f"NOT({ast_to_prefix(node.left)})"
        case NodeType.AND:
            return f"AND({ast_to_prefix(node.left)}, {ast_to_prefix(node.right)})"
        case NodeType.OR:
            return f"OR({ast_to_prefix(node.left)}, {ast_to_prefix(node.right)})"
        case NodeType.IMP:
            return f"IMPLIES({ast_to_prefix(node.left)}, {ast_to_prefix(node.right)})"
        case NodeType.IFF:
            return f"IFF({ast_to_prefix(node.left)}, {ast_to_prefix(node.right)})"
        
def node_to_formula(node: Node) -> Formula:
    match node.type:
        case NodeType.ATOM:
            return Var(node.name)
        case NodeType.TRUE:
            return Var("True")
        case NodeType.FALSE:
            return Var("False")
        case NodeType.NOT:
            return Not(node_to_formula(node.left))
        case NodeType.AND:
            return And(node_to_formula(node.left), node_to_formula(node.right))
        case NodeType.OR:
            return Or(node_to_formula(node.left), node_to_formula(node.right))
        case NodeType.IMP:
            return Imp(node_to_formula(node.left), node_to_formula(node.right))
        case NodeType.IFF:
            return Iff(node_to_formula(node.left), node_to_formula(node.right))