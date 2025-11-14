# Instruções de Instalação e Execução

## Requisitos de Sistema

- **Python:** 3.7 ou superior
- **Sistema Operacional:** Windows, macOS ou Linux
- **Dependências:** Nenhuma (projeto puro Python)

## Instalação

### 1. Extrair o arquivo ZIP

```bash
unzip mini_compiler.zip
cd mini_compiler
```

### 2. Verificar instalação do Python

```bash
python --version
# ou
python3 --version
```

Deve retornar Python 3.7 ou superior.

## Execução

### Opção 1: Usar arquivo de teste padrão

```bash
python main.py
```

Isto compilará o arquivo `tests/programa_ckp2_sexta.mc` (programa válido).

### Opção 2: Compilar arquivo específico

```bash
# Programa com erro (para testar detecção de erros)
python main.py tests/programa_erro.mc

# Arquivo personalizado
python main.py caminho/para/seu/arquivo.mc
```

### Opção 3: Executar testes (requer pytest)

```bash
# Instalar pytest (opcional)
pip install pytest

# Rodar suite de testes
python -m pytest tests/test_parser.py -v

# Ou simplesmente
python tests/test_parser.py
```

## Estrutura de Saída

Após executar, você verá algo como:

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
    3. Token(LPAREN, '(', 1, 14)
    4. Token(RPAREN, ')', 1, 15)
    5. Token(LBRACE, '{', 1, 17)
    6. Token(LET, 'let', 2, 5)
    7. Token(ID, 'x', 2, 9)
    8. Token(COLON, ':', 2, 10)
    9. Token(NUMBER, 'number', 2, 12)
    10. Token(SEMICOLON, ';', 2, 18)
    ... (32 tokens adicionais)

--- Fase 2: Análise Sintática ---
✓ Análise sintática concluída com sucesso!

============================================================
✓ Compilação bem-sucedida!
============================================================
```

## Resolução de Problemas

### Erro: "No module named 'src'"

**Causa:** Python não consegue encontrar o módulo.

**Solução:** Certifique-se de estar na pasta raiz (`mini_compiler/`) ao executar:

```bash
cd mini_compiler
python main.py
```

### Erro: "Arquivo não encontrado"

**Causa:** O caminho do arquivo está incorreto.

**Solução:** Use caminhos relativos a partir da pasta `mini_compiler/`:

```bash
python main.py tests/programa_ckp2_sexta.mc
```

### Erro sintático em programa que deveria ser válido

**Possíveis causas:**
1. Falta de `;` após declaração ou comando
2. Tipo inválido (use `number` ou `float`)
3. Estrutura malformada

**Solução:** Verifique o arquivo de entrada e compare com `tests/programa_ckp2_sexta.mc`.

## Exemplos de Programas Válidos

### Exemplo 1: Programa Simples

```javascript
function main() {
    let x: number;
    x = 42;
    console.log(x);
}
```

### Exemplo 2: Com Condicional

```javascript
function main() {
    let idade: number;
    read(idade);

    if (idade >= 18) {
        console.log("Maior de idade");
    } else {
        console.log("Menor de idade");
    }
}
```

### Exemplo 3: Com Repetição

```javascript
function main() {
    let i: number;
    let soma: float;

    i = 0;
    soma = 0.0;

    while (i < 10) {
        soma = soma + i;
        i = i + 1;
    }

    console.log(soma);
}
```

### Exemplo 4: Expressões Complexas

```javascript
function main() {
    let a: number;
    let b: number;
    let resultado: float;

    read(a);
    read(b);

    resultado = (a + b) * 2 - 5 / 2;

    if (resultado > 100 && resultado < 1000) {
        console.log("Valor válido");
    }
}
```

## Exemplos de Erros Detectados

### Erro 1: Falta de `;`

```javascript
function main() {
    let x: number    // ← Falta ;
}
```

**Mensagem:** `Erro Sintático na linha 2, coluna 20: Esperado SEMICOLON, encontrado RBRACE`

### Erro 2: Tipo Inválido

```javascript
function main() {
    let x: integer;  // ← integer não existe
}
```

**Mensagem:** `Erro Sintático na linha 2, coluna 12: Tipo inválido: esperado 'number' ou 'float'`

### Erro 3: Estrutura Malformada

```javascript
function main() {
    if x > 0 {       // ← Falta ( )
        console.log("ok");
    }
}
```

**Mensagem:** `Erro Sintático na linha 2, coluna 8: Esperado LPAREN, encontrado ID`

## Desenvolvimento e Testes

### Rodar todos os testes

```bash
python tests/test_parser.py
```

### Criar novo arquivo de teste

1. Crie um arquivo com extensão `.mc` na pasta `tests/`
2. Escreva seu código seguindo a gramática
3. Execute:

```bash
python main.py tests/seu_arquivo.mc
```

### Debug

Para adicionar prints de debug no parser, edite `src/parser.py` e adicione:

```python
def programa(self):
    print(f"DEBUG: Iniciando análise de programa")
    print(f"DEBUG: Token atual: {self.current_token}")
    # ... resto do código
```

## Estrutura do Código

### Fluxo de Compilação

```
entrada.mc
    ↓
[Lexer]        → tokenize()     → Lista de Tokens
    ↓
[Parser]       → parse()        → Aceita/Rejeita
    ↓
[Saída]        → Mensagem de Sucesso ou Erro
```

### Arquivos Principais

| Arquivo | Função |
|---------|--------|
| `main.py` | Ponto de entrada |
| `src/lexer.py` | Análise Léxica |
| `src/parser.py` | Análise Sintática |
| `src/token_types.py` | Definição de tokens |
| `tests/test_parser.py` | Suite de testes |

## Próximos Passos

Para estender o compilador:

1. **Análise Semântica:** Implementar type checking e validações
2. **Geração de Código:** Produzir código intermediário ou executável
3. **Otimização:** Aplicar técnicas de otimização
4. **Novos Features:** Adicionar funções, arrays, structs, etc.

## Suporte

Para dúvidas ou problemas:

1. Consulte a documentação em `docs/`
2. Verifique os exemplos em `tests/`
3. Examine o código-fonte comentado
