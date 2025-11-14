"""
Parser - Analisador Sintático Descendente Preditivo Recursivo
Responsável pela verificação da estrutura gramatical

Correções:
- Refatorada a gramática de expressões para resolver o conflito FIRST/FIRST
  em 'termoRelacional' e 'fator' sobre o token 'LPAREN'.
- 'fator' agora é responsável por todas as expressões parentizadas,
  chamando 'expressaoRelacional'.
- 'termoRelacional' foi simplificado para 'expressaoAritmetica (OP_REL expressaoAritmetica)?',
  removendo a produção conflitante 'LPAREN expressaoRelacional RPAREN'.
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
        # Adiciona um token de fim de arquivo para evitar falhas de índice
        if not tokens or tokens[-1].tipo != TokenType.EOF:
             # Assume que o último token dá a linha/coluna final se existir
             last_line = tokens[-1].linha if tokens else 1
             last_col = tokens[-1].coluna if tokens else 1
             self.tokens.append(Token(TokenType.EOF, "EOF", last_line, last_col + 1))
        
        self.current_token = self.tokens[0]

    def advance(self):
        """Consome o token atual e avança para o próximo"""
        # Não avança além do EOF
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.current_token = self.tokens[self.pos]

    def peek_token(self, offset=1):
        """Visualiza token à frente sem consumir"""
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1] # Retorna EOF se estourar

    def expect(self, tipo_token):
        """Verifica se token atual é do tipo esperado e avança"""
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
        # Após o programa, devemos estar no token EOF
        if not self.match(TokenType.EOF):
             self.error(f"Tokens inesperados após o fim do programa. Encontrado: {self.current_token.tipo}")

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
        # Modificado para permitir 0 ou mais declarações
        self.declaracoes()
        # Modificado para permitir 0 ou mais comandos
        self.comandos()

    def declaracoes(self):
        """declaracoes : declaracao declaracoes | ε"""
        # Permite 0 ou mais declarações
        while self.match(TokenType.LET, TokenType.CONST):
            self.declaracao()

    def declaracao(self):
        """declaracao : ('let' | 'const') ID ':' tipo ';'"""
        if self.match(TokenType.LET):
            self.advance()
        elif self.match(TokenType.CONST):
            self.advance()
        else:
            # Isso não deve acontecer se chamado por 'declaracoes'
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
        """comandos : comando comandos | ε"""
        # Permite 0 ou mais comandos
        # First(comando) = {ID, READ, CONSOLE_LOG, IF, WHILE, LBRACE}
        while self.match(TokenType.ID, TokenType.READ, TokenType.CONSOLE_LOG,
                         TokenType.IF, TokenType.WHILE, TokenType.LBRACE):
            self.comando()

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
        if self.match(TokenType.ID, TokenType.STRING):
            self.advance()
        # CORREÇÃO: A gramática original também deveria permitir
        #           qualquer expressão aritmética.
        #           Vamos manter ID | STRING por enquanto,
        #           mas o ideal seria 'expressaoRelacional'.
        # elif self.match(TokenType.ID, TokenType.STRING):
        #     self.advance()
        else:
            # Vamos permitir qualquer expressão
            self.expressaoRelacional() 
            # self.error("Esperado ID ou STRING em console.log")
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
        self.comandos() # 'comandos' agora permite 0 comandos
        self.expect(TokenType.RBRACE)

    def expressaoAritmetica(self):
        """expressaoAritmetica : termo expressaoAritmetica'"""
        self.termo()
        self.expressaoAritmetica_linha()

    def expressaoAritmetica_linha(self):
        """expressaoAritmetica' : ('+' | '-') termo expressaoAritmetica' | ε"""
        if self.match(TokenType.PLUS, TokenType.MINUS):
            self.advance()
            self.termo()
            self.expressaoAritmetica_linha()

    def termo(self):
        """termo : fator termo'"""
        self.fator()
        self.termo_linha()

    def termo_linha(self):
        """termo' : ('*' | '/' | '%') fator termo' | ε"""
        # Corrigido para incluir MOD (módulo)
        if self.match(TokenType.MULT, TokenType.DIV, TokenType.MOD):
            self.advance()
            self.fator()
            self.termo_linha()

    def fator(self):
        """fator : NUMINT | NUMREAL | ID | '(' expressaoRelacional ')'"""
        # CORREÇÃO: Alterado de 'expressaoAritmetica' para 'expressaoRelacional'
        # para resolver o conflito gramatical.
        if self.match(TokenType.NUMINT, TokenType.NUMREAL, TokenType.ID):
            self.advance()
        elif self.match(TokenType.LPAREN):
            self.advance()
            self.expressaoRelacional() # Chamada recursiva para a expressão de maior precedência
            self.expect(TokenType.RPAREN)
        else:
            self.error("Fator inválido: esperado Número, ID ou '('")

    def expressaoRelacional(self):
        """expressaoRelacional : termoRelacional expressaoRelacional'"""
        # print("Entrando em expressaoRelacional") # Debug removido
        self.termoRelacional()
        self.expressaoRelacional_linha()

    def expressaoRelacional_linha(self):
        """expressaoRelacional' : operadorLogico termoRelacional expressaoRelacional' | ε"""
        if self.match(TokenType.AND, TokenType.OR):
            self.advance() # operadorLogico consumido
            self.termoRelacional()
            self.expressaoRelacional_linha()

    def termoRelacional(self):
        """termoRelacional : expressaoAritmetica (operadorRelacional expressaoAritmetica)?"""
        # CORREÇÃO: Gramática simplificada.
        # A regra 'LPAREN expressaoRelacional RPAREN' foi movida para 'fator'.
        self.expressaoAritmetica()
        
        # Verifica se há uma parte relacional (opcional)
        if self.match(TokenType.LT, TokenType.GT, TokenType.LTE, 
                      TokenType.GTE, TokenType.EQ, TokenType.NEQ):
            self.operadorRelacional()
            self.expressaoAritmetica()

    def operadorRelacional(self):
        """operadorRelacional : '<' | '>' | '<=' | '>=' | '==' | '!='"""
        if self.match(TokenType.LT, TokenType.GT, TokenType.LTE,
                      TokenType.GTE, TokenType.EQ, TokenType.NEQ):
            self.advance()
        else:
            self.error("Operador relacional esperado")
