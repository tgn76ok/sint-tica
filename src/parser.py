"""
Parser - Analisador Sintático Descendente Preditivo Recursivo
Responsável pela verificação da estrutura gramatical
"""

from .token_types import Token, TokenType


class SyntaxError(Exception):
    """Exceção de erro sintático"""
    def __init__(self, message, token):
        self.message = message
        self.token = token
        self.linha = token.linha
        self.coluna = token.coluna

    def __str__(self):
        return f"Erro Sintático na linha {self.linha}, coluna {self.coluna}: {self.message}\n  Token: {self.token.valor}"


class Parser:
    """Analisador Sintático Descendente Preditivo Recursivo"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[0] if tokens else None

    def advance(self):
        """Consome o token atual e avança para o próximo"""
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]

    def peek_token(self, offset=1):
        """Visualiza token à frente sem consumir"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None

    def expect(self, tipo_token):
        """Verifica se token atual é do tipo esperado"""
        if self.current_token.tipo != tipo_token:
            raise SyntaxError(
                f"Esperado {tipo_token}, encontrado {self.current_token.tipo}",
                self.current_token
            )
        token = self.current_token
        self.advance()
        return token

    def match(self, *tipos):
        """Verifica se token atual é um dos tipos dados"""
        return self.current_token.tipo in tipos

    def error(self, message):
        """Lança erro sintático"""
        raise SyntaxError(message, self.current_token)

    # Procedimentos recursivos para cada não-terminal

    def parse(self):
        """Inicia a análise"""
        self.programa()

    def programa(self):
        """programa : 'function' 'main' '(' ')' '{' corpo '}'"""
        self.expect(TokenType.FUNCTION)
        self.expect(TokenType.MAIN)
        self.expect(TokenType.LPAREN)
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.LBRACE)
        self.corpo()
        self.expect(TokenType.RBRACE)

    def corpo(self):
        """corpo : declaracoes comandos"""
        self.declaracoes()
        self.comandos()

    def declaracoes(self):
        """declaracoes : declaracao declaracoes | declaracao"""
        self.declaracao()
        # Verifica se há mais declarações
        if self.match(TokenType.LET, TokenType.CONST):
            self.declaracoes()

    def declaracao(self):
        """declaracao : ('let' | 'const') ID ':' tipo ';'"""
        if self.match(TokenType.LET):
            self.advance()
        elif self.match(TokenType.CONST):
            self.advance()
        else:
            self.error("Esperado 'let' ou 'const'")

        self.expect(TokenType.ID)
        self.expect(TokenType.COLON)
        self.tipo()
        self.expect(TokenType.SEMICOLON)

    def tipo(self):
        """tipo : 'number' | 'float'"""
        if self.match(TokenType.NUMBER):
            self.advance()
        elif self.match(TokenType.FLOAT):
            self.advance()
        else:
            self.error("Tipo inválido: esperado 'number' ou 'float'")

    def comandos(self):
        """comandos : comando comandos | comando"""
        self.comando()
        # First(comando) = {ID, READ, CONSOLE_LOG, IF, WHILE, LBRACE}
        if self.match(TokenType.ID, TokenType.READ, TokenType.CONSOLE_LOG,
                      TokenType.IF, TokenType.WHILE, TokenType.LBRACE):
            self.comandos()

    def comando(self):
        """comando : atribuicao | leitura | escrita | condicional | repeticao | blocoInterno"""
        if self.match(TokenType.ID):
            self.atribuicao()
        elif self.match(TokenType.READ):
            self.leitura()
        elif self.match(TokenType.CONSOLE_LOG):
            self.escrita()
        elif self.match(TokenType.IF):
            self.condicional()
        elif self.match(TokenType.WHILE):
            self.repeticao()
        elif self.match(TokenType.LBRACE):
            self.blocoInterno()
        else:
            self.error("Comando inválido")

    def atribuicao(self):
        """atribuicao : ID '=' expressaoAritmetica ';'"""
        self.expect(TokenType.ID)
        self.expect(TokenType.ASSIGN)
        self.expressaoAritmetica()
        self.expect(TokenType.SEMICOLON)

    def leitura(self):
        """leitura : 'read' '(' ID ')' ';'"""
        self.expect(TokenType.READ)
        self.expect(TokenType.LPAREN)
        self.expect(TokenType.ID)
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)

    def escrita(self):
        """escrita : 'console.log' '(' (ID | STRING) ')' ';'"""
        self.expect(TokenType.CONSOLE_LOG)
        self.expect(TokenType.LPAREN)
        if self.match(TokenType.ID):
            self.advance()
        elif self.match(TokenType.STRING):
            self.advance()
        else:
            self.error("Esperado ID ou STRING em console.log")
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)

    def condicional(self):
        """condicional : 'if' '(' expressaoRelacional ')' blocoInterno
                       | 'if' '(' expressaoRelacional ')' blocoInterno 'else' blocoInterno"""
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        self.expressaoRelacional()
        self.expect(TokenType.RPAREN)
        self.blocoInterno()

        if self.match(TokenType.ELSE):
            self.advance()
            self.blocoInterno()

    def repeticao(self):
        """repeticao : 'while' '(' expressaoRelacional ')' blocoInterno"""
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        self.expressaoRelacional()
        self.expect(TokenType.RPAREN)
        self.blocoInterno()

    def blocoInterno(self):
        """blocoInterno : '{' comandos '}'"""
        self.expect(TokenType.LBRACE)
        self.comandos()
        self.expect(TokenType.RBRACE)

    def expressaoAritmetica(self):
        """expressaoAritmetica : termo expressaoAritmetica'
           Eliminação de recursão à esquerda"""
        self.termo()
        self.expressaoAritmetica_linha()

    def expressaoAritmetica_linha(self):
        """expressaoAritmetica' : ('+' | '-') termo expressaoAritmetica' | ε"""
        if self.match(TokenType.PLUS, TokenType.MINUS):
            self.advance()
            self.termo()
            self.expressaoAritmetica_linha()

    def termo(self):
        """termo : fator termo'
           Eliminação de recursão à esquerda"""
        self.fator()
        self.termo_linha()

    def termo_linha(self):
        """termo' : ('*' | '/') fator termo' | ε"""
        if self.match(TokenType.MULT, TokenType.DIV, TokenType.MOD):
            self.advance()
            self.fator()
            self.termo_linha()

    def fator(self):
        """fator : NUMINT | NUMREAL | ID | '(' expressaoAritmetica ')'"""
        if self.match(TokenType.NUMINT, TokenType.NUMREAL, TokenType.ID):
            self.advance()
        elif self.match(TokenType.LPAREN):
            self.advance()
            self.expressaoAritmetica()
            self.expect(TokenType.RPAREN)
        else:
            self.error("Fator inválido")

    def expressaoRelacional(self):
        """expressaoRelacional : termoRelacional expressaoRelacional'
           Eliminação de recursão à esquerda"""
        self.termoRelacional()
        self.expressaoRelacional_linha()

    def expressaoRelacional_linha(self):
        """expressaoRelacional' : operadorLogico termoRelacional expressaoRelacional' | ε"""
        if self.match(TokenType.AND, TokenType.OR):
            self.advance()
            self.termoRelacional()
            self.expressaoRelacional_linha()

    def termoRelacional(self):
        """termoRelacional : expressaoAritmetica OP_REL expressaoAritmetica
                           | '(' expressaoRelacional ')'"""
        if self.match(TokenType.LPAREN):
            self.advance()
            self.expressaoRelacional()
            self.expect(TokenType.RPAREN)
        else:
            self.expressaoAritmetica()
            self.operadorRelacional()
            self.expressaoAritmetica()

    def operadorRelacional(self):
        """operadorRelacional : '<' | '>' | '<=' | '>=' | '==' | '!='"""
        if self.match(TokenType.LT, TokenType.GT, TokenType.LTE,
                      TokenType.GTE, TokenType.EQ, TokenType.NEQ):
            self.advance()
        else:
            self.error("Operador relacional esperado")
