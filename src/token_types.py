"""
Token Types - Definição dos tipos de tokens suportados
"""

class TokenType:
    # Palavras reservadas
    FUNCTION = "FUNCTION"
    MAIN = "MAIN"
    LET = "LET"
    CONST = "CONST"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    READ = "READ"
    CONSOLE_LOG = "CONSOLE_LOG"

    # Tipos
    NUMBER = "NUMBER"
    FLOAT = "FLOAT"

    # Operadores aritméticos
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULT = "MULT"
    DIV = "DIV"
    MOD = "MOD"

    # Operadores relacionais
    LT = "LT"           # <
    GT = "GT"           # >
    LTE = "LTE"         # <=
    GTE = "GTE"         # >=
    EQ = "EQ"           # ==
    NEQ = "NEQ"         # !=

    # Operadores lógicos
    AND = "AND"         # &&
    OR = "OR"           # ||
    NOT = "NOT"         # !

    # Delimitadores
    LPAREN = "LPAREN"           # (
    RPAREN = "RPAREN"           # )
    LBRACE = "LBRACE"           # {
    RBRACE = "RBRACE"           # }
    SEMICOLON = "SEMICOLON"     # ;
    COLON = "COLON"             # :
    ASSIGN = "ASSIGN"           # =

    # Literais e identificadores
    ID = "ID"
    NUMINT = "NUMINT"
    NUMREAL = "NUMREAL"
    STRING = "STRING"

    # Special
    EOF = "EOF"
    ERROR = "ERROR"


class Token:
    def __init__(self, tipo, valor, linha, coluna):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        return f"Token({self.tipo}, {repr(self.valor)}, {self.linha}, {self.coluna})"

    def __str__(self):
        return f"[{self.tipo}] {self.valor} (linha {self.linha}, col {self.coluna})"
