"""
Lexer - Analisador Léxico
Responsável pela tokenização do código-fonte
"""

import re
from .token_types import Token, TokenType


class Lexer:
    PALAVRAS_RESERVADAS = {
        'function': TokenType.FUNCTION,
        'main': TokenType.MAIN,
        'let': TokenType.LET,
        'const': TokenType.CONST,
        'if': TokenType.IF,
        'else': TokenType.ELSE,
        'while': TokenType.WHILE,
        'read': TokenType.READ,
        'console.log': TokenType.CONSOLE_LOG,
        'number': TokenType.NUMBER,
        'float': TokenType.FLOAT,
    }

    def __init__(self, codigo_fonte):
        self.codigo = codigo_fonte
        self.pos = 0
        self.linha = 1
        self.coluna = 1
        self.tokens = []

    def error(self, msg):
        raise SyntaxError(f"Erro Léxico na linha {self.linha}, coluna {self.coluna}: {msg}")

    def peek(self, offset=0):
        """Retorna caractere sem avançar"""
        pos = self.pos + offset
        if pos < len(self.codigo):
            return self.codigo[pos]
        return None

    def advance(self):
        """Avança para o próximo caractere"""
        if self.pos < len(self.codigo):
            if self.codigo[self.pos] == '\n':
                self.linha += 1
                self.coluna = 1
            else:
                self.coluna += 1
            self.pos += 1

    def skip_whitespace(self):
        """Ignora espaços em branco e comentários"""

        while self.pos < len(self.codigo):
            if self.codigo[self.pos].isspace():
                self.advance()
            elif self.codigo[self.pos:self.pos+2] == '//':
                # Comentário de linha
                while self.pos < len(self.codigo) and self.codigo[self.pos] != '\n':
                    self.advance()
            elif self.codigo[self.pos:self.pos+2] == '/*':
                # Comentário de bloco
                self.advance()
                self.advance()
                while self.pos < len(self.codigo) - 1:
                    if self.codigo[self.pos:self.pos+2] == '*/':
                        self.advance()
                        self.advance()
                        break
                    self.advance()
            else:
                break

    def read_number(self):
        """Lê número inteiro ou real"""
        inicio_linha = self.linha
        inicio_coluna = self.coluna
        num_str = ''

        while self.peek() and self.peek().isdigit():
            num_str += self.peek()
            self.advance()

        # Verifica número real
        if self.peek() == '.' and self.peek(1) and self.peek(1).isdigit():
            num_str += self.peek()  # adiciona ponto
            self.advance()
            while self.peek() and self.peek().isdigit():
                num_str += self.peek()
                self.advance()
            return Token(TokenType.NUMREAL, float(num_str), inicio_linha, inicio_coluna)

        return Token(TokenType.NUMINT, int(num_str), inicio_linha, inicio_coluna)

    def read_string(self, delimiter):
        """Lê string"""
        inicio_linha = self.linha
        inicio_coluna = self.coluna
        self.advance()  # pula delimitador inicial
        string = ''

        while self.peek() and self.peek() != delimiter:
            if self.peek() == '\\':
                self.advance()
                if self.peek():
                    # Escape sequences
                    escape_map = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'"}
                    string += escape_map.get(self.peek(), self.peek())
                    self.advance()
            else:
                string += self.peek()
                self.advance()

        if self.peek() == delimiter:
            self.advance()  # pula delimitador final
        else:
            self.error(f"String não terminada")

        return Token(TokenType.STRING, string, inicio_linha, inicio_coluna)

    def read_identifier(self):
        """Lê identificador ou palavra reservada"""
        inicio_linha = self.linha
        inicio_coluna = self.coluna
        ident = ''

        while self.peek() and (self.peek().isalnum() or self.peek() in '_'):
            ident += self.peek()
            self.advance()

        # Verifica console.log
        if ident == 'console' and self.peek() == '.':
            self.advance()
            ident += '.'
            while self.peek() and self.peek().isalnum():
                ident += self.peek()
                self.advance()

        tipo_token = self.PALAVRAS_RESERVADAS.get(ident, TokenType.ID)
        return Token(tipo_token, ident, inicio_linha, inicio_coluna)

    def tokenize(self):
        """Realiza a tokenização completa"""
        while self.pos < len(self.codigo):
            self.skip_whitespace()

            if self.pos >= len(self.codigo):
                break

            char = self.peek()
            linha = self.linha
            coluna = self.coluna

            # Números
            if char.isdigit():
                self.tokens.append(self.read_number())

            # Strings
            elif char in ('"', "'"):
                self.tokens.append(self.read_string(char))

            # Identificadores e palavras reservadas
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())

            # Operadores e delimitadores
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', linha, coluna))
                self.advance()

            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', linha, coluna))
                self.advance()

            elif char == '*':
                self.tokens.append(Token(TokenType.MULT, '*', linha, coluna))
                self.advance()

            elif char == '/':
                self.tokens.append(Token(TokenType.DIV, '/', linha, coluna))
                self.advance()
                
            elif char == '%':
                self.tokens.append(Token(TokenType.MOD, '%', linha, coluna))
                self.advance()
                
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', linha, coluna))
                self.advance()

            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', linha, coluna))
                self.advance()

            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', linha, coluna))
                self.advance()

            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', linha, coluna))
                self.advance()

            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', linha, coluna))
                self.advance()

            elif char == ':':
                self.tokens.append(Token(TokenType.COLON, ':', linha, coluna))
                self.advance()

            elif char == '=':
                if self.peek(1) == '=':
                    self.tokens.append(Token(TokenType.EQ, '==', linha, coluna))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', linha, coluna))
                    self.advance()

            elif char == '<':
                if self.peek(1) == '=':
                    self.tokens.append(Token(TokenType.LTE, '<=', linha, coluna))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.LT, '<', linha, coluna))
                    self.advance()

            elif char == '>':
                if self.peek(1) == '=':
                    self.tokens.append(Token(TokenType.GTE, '>=', linha, coluna))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.GT, '>', linha, coluna))
                    self.advance()

            elif char == '!':
                if self.peek(1) == '=':
                    self.tokens.append(Token(TokenType.NEQ, '!=', linha, coluna))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.NOT, '!', linha, coluna))
                    self.advance()

            elif char == '&':
                if self.peek(1) == '&':
                    self.tokens.append(Token(TokenType.AND, '&&', linha, coluna))
                    self.advance()
                    self.advance()
                else:
                    self.error(f"Caractere inesperado: {char}")

            elif char == '|':
                if self.peek(1) == '|':
                    self.tokens.append(Token(TokenType.OR, '||', linha, coluna))
                    self.advance()
                    self.advance()
                else:
                    self.error(f"Caractere inesperado: {char}")

            else:
                self.error(f"Caractere não reconhecido: {char}")

        # Adiciona token EOF
        self.tokens.append(Token(TokenType.EOF, '', self.linha, self.coluna))
        return self.tokens
