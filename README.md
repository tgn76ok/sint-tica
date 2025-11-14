# Mini Compiler - Checkpoint 02

Implementação de um **Analisador Sintático Descendente Preditivo Recursivo** para uma linguagem imperativa simples.

## Estrutura do Projeto

```
mini_compiler/
├── src/
│   ├── __init__.py           # Pacote SRC
│   ├── token_types.py        # Definição de tipos de tokens
│   ├── lexer.py              # Analisador Léxico (Checkpoint 01)
│   └── parser.py             # Analisador Sintático (Checkpoint 02)
├── tests/
│   ├── programa_ckp2_sexta.mc   # Programa de teste válido
│   └── programa_erro.mc         # Programa com erros sintáticos
├── docs/
│   ├── gramatica.txt         # Especificação da gramática
│   ├── grafos_sintaticos.md  # Grafos sintáticos
│   └── arquitetura.md        # Documentação da arquitetura
├── main.py                   # Ponto de entrada
└── README.md                 # Este arquivo
```

## Requisitos

- Python 3.7+
- Nenhuma dependência externa

## Instalação

```bash
# Clonar ou extrair o projeto
cd mini_compiler

# Não há necessidade de instalação adicional
```

## Uso

### Compilar um arquivo

```bash
# Usar arquivo padrão de teste
python main.py

# Especificar arquivo personalizado
python main.py tests/programa_ckp2_sexta.mc
python main.py tests/programa_erro.mc
```

### Exemplo de Saída (Sucesso)

```
============================================================
Compilador MiniLanguage
============================================================

Arquivo: tests/programa_ckp2_sexta.mc
✓ Arquivo lido com sucesso (285 caracteres)

--- Fase 1: Análise Léxica ---
✓ Análise léxica concluída
  Total de tokens: 42

  Primeiros tokens:
    1. Token(FUNCTION, 'function', 1, 1)
    2. Token(MAIN, 'main', 1, 10)
    ...

--- Fase 2: Análise Sintática ---
✓ Análise sintática concluída com sucesso!

============================================================
✓ Compilação bem-sucedida!
============================================================
```

### Exemplo de Saída (Erro)

```
✗ Erro Sintático na linha 2, coluna 25: Esperado SEMICOLON, encontrado LET
  Token: let
```

## Gramática Suportada

A linguagem suporta a seguinte gramática BNF:

```
programa       → 'function' 'main' '(' ')' '{' corpo '}'
corpo          → declaracoes comandos
declaracoes    → declaracao | declaracao declaracoes
declaracao     → ('let' | 'const') ID ':' tipo ';'
tipo           → 'number' | 'float'
comandos       → comando | comando comandos
comando        → atribuicao | leitura | escrita | condicional | repeticao | blocoInterno
atribuicao     → ID '=' expressaoAritmetica ';'
leitura        → 'read' '(' ID ')' ';'
escrita        → 'console.log' '(' (ID | STRING) ')' ';'
condicional    → 'if' '(' expressaoRelacional ')' blocoInterno
               | 'if' '(' expressaoRelacional ')' blocoInterno 'else' blocoInterno
repeticao      → 'while' '(' expressaoRelacional ')' blocoInterno
blocoInterno   → '{' comandos '}'
expressaoAritmetica → expressaoAritmetica '+' termo
                    | expressaoAritmetica '-' termo
                    | termo
termo          → termo '*' fator
               | termo '/' fator
               | fator
fator          → NUMINT | NUMREAL | ID | '(' expressaoAritmetica ')'
expressaoRelacional → expressaoAritmetica OP_REL expressaoAritmetica
                    | '(' expressaoRelacional ')'
                    | expressaoRelacional operadorLogico termoRelacional
termoRelacional → expressaoAritmetica OP_REL expressaoAritmetica
                | '(' expressaoRelacional ')'
operadorLogico → '&&' | '||'
```

Onde OP_REL = `<` | `>` | `<=` | `>=` | `==` | `!=`

## Tipos de Tokens

### Palavras Reservadas
- `function`, `main` - Estrutura do programa
- `let`, `const` - Declarações de variáveis
- `number`, `float` - Tipos de dados
- `if`, `else` - Estruturas condicionais
- `while` - Estrutura de repetição
- `read` - Entrada de dados
- `console.log` - Saída de dados

### Operadores
- Aritméticos: `+`, `-`, `*`, `/`
- Relacionais: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Lógicos: `&&`, `||`, `!`
- Atribuição: `=`

### Delimitadores
- `(`, `)` - Parênteses
- `{`, `}` - Chaves
- `;` - Ponto e vírgula
- `:` - Dois-pontos

### Literais
- `NUMINT` - Números inteiros (ex: 42)
- `NUMREAL` - Números reais (ex: 3.14)
- `ID` - Identificadores (ex: x, variavel1)
- `STRING` - Cadeias de caracteres (ex: "Olá")

## Fases da Compilação

### 1. Análise Léxica (Lexer)
- Lê o código-fonte caractere por caractere
- Identifica lexemas (palavras, números, operadores, etc.)
- Gera uma sequência de tokens
- Realiza validação léxica básica

**Saída:** Stream de tokens com tipo, valor, linha e coluna

### 2. Análise Sintática (Parser)
- Recebe os tokens do lexer
- Verifica se seguem as regras gramaticais
- Utiliza abordagem descendente preditiva recursiva
- Um procedimento recursivo para cada não-terminal da gramática

**Saída:** Aceita/rejeita o programa com mensagens de erro detalhadas

## Tratamento de Erros

O compilador fornece mensagens de erro detalhadas incluindo:
- Linha e coluna do erro
- Token encontrado e esperado
- Tipo de erro sintático

Exemplo:
```
Erro Sintático na linha 5, coluna 15: Esperado SEMICOLON, encontrado READ
  Token: read
```

## Estratégias de Parsing

### Análise Descendente Preditiva Recursiva
- Começa pelo símbolo inicial (programa)
- Expande top-down até terminais
- Usa lookahead de 1 token para decisões preditivas
- Sem retrocesso (determinístico)
- Baseia-se em conjuntos **First** e **Follow**

### Eliminação de Recursão à Esquerda
Para evitar loops infinitos, as seguintes produções foram transformadas:

**Original:**
```
expressaoAritmetica → expressaoAritmetica '+' termo
                    | expressaoAritmetica '-' termo
                    | termo
```

**Transformada:**
```
expressaoAritmetica → termo expressaoAritmetica'
expressaoAritmetica' → '+' termo expressaoAritmetica'
                     | '-' termo expressaoAritmetica'
                     | ε
```

## Exemplos

### Programa Válido
```javascript
function main() {
    let x: number;
    let y: float;

    read(x);
    y = x * 2 + 5.5;

    if (x > 0) {
        console.log("Positivo");
    } else {
        console.log("Não positivo");
    }

    while (x < 100) {
        x = x + 1;
    }
}
```

### Erros Detectados
- Falta de ponto-e-vírgula
- Tipos inválidos
- Estruturas malformadas
- Operadores faltantes
- Delimitadores não balanceados

## Contribuidores

- Desenvolvido para disciplina de Construção de Compiladores I
- Checkpoint 02 - Análise Sintática

## Licença

Projeto acadêmico - Uso para fins educacionais
