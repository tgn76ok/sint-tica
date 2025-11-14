# Grafos Sintáticos - Mini Language

## Representação Visual das Produções Gramaticais

Os grafos sintáticos (também chamados de diagramas de sintaxe ou railroad diagrams) representam visualmente as produções da gramática. Cada gráfo mostra o fluxo de análise para um não-terminal.

## 1. Gráfo: programa

```
┌─────────────────────────────────────────────┐
│                 programa                    │
└─────────────────────────────────────────────┘
   │
   ├─ 'function' ──→ 'main' ──→ '(' ──→ ')' ──→ '{' ──→ corpo ──→ '}' ──→ ✓
```

## 2. Gráfo: corpo

```
┌─────────────────────────────────────────────┐
│                   corpo                     │
└─────────────────────────────────────────────┘
   │
   ├─ declaracoes ──→ comandos ──→ ✓
```

## 3. Gráfo: declaracoes (com recursão)

```
┌─────────────────────────────────────────────┐
│                 declaracoes                 │
└─────────────────────────────────────────────┘
   │
   ├─ declaracao ──┐
   │              │
   │      ┌───────┴─── (opcional)
   │      │
   │      └─ declaracao ──┐
   │                      │
   │          ┌───────────┴─── (repete)
   │          └──────↑
   │                 │
   └─────────────────┘ ──→ ✓
```

## 4. Gráfo: declaracao

```
┌─────────────────────────────────────────────┐
│                 declaracao                  │
└─────────────────────────────────────────────┘
   │
   ├─┬──'let'
   │ │         ──→ ID ──→ ':' ──→ tipo ──→ ';' ──→ ✓
   │ └──'const'
   │
```

## 5. Gráfo: tipo

```
┌─────────────────────────────────────────────┐
│                   tipo                      │
└─────────────────────────────────────────────┘
   │
   ├─┬──'number' ──→ ✓
   │ │
   │ └──'float' ──→ ✓
```

## 6. Gráfo: comando (alternativa)

```
┌─────────────────────────────────────────────┐
│                  comando                    │
└─────────────────────────────────────────────┘
   │
   ├─ atribuicao ────────────┐
   │                         │
   ├─ leitura ───────────────┤
   │                         ├──→ ✓
   ├─ escrita ───────────────┤
   │                         │
   ├─ condicional ───────────┤
   │                         │
   ├─ repeticao ─────────────┤
   │                         │
   └─ blocoInterno ──────────┘
```

## 7. Gráfo: expressaoAritmetica (após eliminação de recursão)

```
┌──────────────────────────────────────────────────┐
│            expressaoAritmetica                   │
└──────────────────────────────────────────────────┘
   │
   ├─ termo ──→ expressaoAritmetica' ──→ ✓
                       │
            ┌──────────┴──────────┐
            │                     │
      ┌─────┴────┐               │
      │           │              │
  ┌─ '+' ─┐   ┌─ '-' ─┐         │
  │       │   │       │      ┌──┴──┐
  └───┬───┘   └───┬───┘      │ ε   │
      │           │          │(fim)│
      └─ termo ───┘          └─────┘
      │           │
      └───────┬───┘
              │
         (repete)
```

## 8. Gráfo: expressaoRelacional

```
┌──────────────────────────────────────────────────┐
│             expressaoRelacional                  │
└──────────────────────────────────────────────────┘
   │
   ├─ termoRelacional ──→ expressaoRelacional' ──→ ✓
                                  │
                      ┌───────────┴───────────┐
                      │                       │
                  ┌─ '&&' ─┐   ┌─ '||' ─┐   │
                  │        │   │        │   │
                  └───┬────┘   └───┬────┘   │
                      │            │       │
                      └─ termoRelacional
                      │            │       │
                      └───────┬────┘   ┌──┴──┐
                          (repete)     │ ε   │
                                       └─────┘
```

## 9. Gráfo: termoRelacional

```
┌──────────────────────────────────────────────────┐
│             termoRelacional                      │
└──────────────────────────────────────────────────┘
   │
   ├─┬─ '(' ──→ expressaoRelacional ──→ ')' ──→ ✓
   │ │
   │ └─ expressaoAritmetica ──→ OP_REL ──→ expressaoAritmetica ──→ ✓
```

## 10. Gráfo: fator

```
┌──────────────────────────────────────────────────┐
│                   fator                          │
└──────────────────────────────────────────────────┘
   │
   ├─ NUMINT ────────────────────────┐
   │                                 │
   ├─ NUMREAL ───────────────────────┤
   │                                 ├──→ ✓
   ├─ ID ────────────────────────────┤
   │                                 │
   └─ '(' ──→ expressaoAritmetica ──→ ')' ┘
```

## 11. Gráfo: atribuicao

```
┌──────────────────────────────────────────────────┐
│               atribuicao                         │
└──────────────────────────────────────────────────┘
   │
   ├─ ID ──→ '=' ──→ expressaoAritmetica ──→ ';' ──→ ✓
```

## 12. Gráfo: leitura

```
┌──────────────────────────────────────────────────┐
│                 leitura                          │
└──────────────────────────────────────────────────┘
   │
   ├─ 'read' ──→ '(' ──→ ID ──→ ')' ──→ ';' ──→ ✓
```

## 13. Gráfo: escrita

```
┌──────────────────────────────────────────────────┐
│                 escrita                          │
└──────────────────────────────────────────────────┘
   │
   ├─ 'console.log' ──→ '(' ──→ ┬─ ID ──┬ ──→ ')' ──→ ';' ──→ ✓
   │                           └─ STRING ┘
```

## 14. Gráfo: condicional

```
┌──────────────────────────────────────────────────┐
│               condicional                        │
└──────────────────────────────────────────────────┘
   │
   ├─ 'if' ──→ '(' ──→ expressaoRelacional ──→ ')' ──→ blocoInterno ──┐
   │                                                                    │
   │                                       ┌──────────────────────────┘
   │                                       │
   │                                  ┌────┴────┐
   │                                  │          │
   │                              ┌──'else'──┐   │
   │                              │          │   │
   │                              └─ blocoInterno ┐
   │                                          │   │
   └──────────────────────────────────────────┴───→ ✓
```

## 15. Gráfo: repeticao

```
┌──────────────────────────────────────────────────┐
│                 repeticao                        │
└──────────────────────────────────────────────────┘
   │
   ├─ 'while' ──→ '(' ──→ expressaoRelacional ──→ ')' ──→ blocoInterno ──→ ✓
```

## 16. Gráfo: blocoInterno

```
┌──────────────────────────────────────────────────┐
│               blocoInterno                       │
└──────────────────────────────────────────────────┘
   │
   ├─ '{' ──→ comandos ──→ '}' ──→ ✓
```

## Legenda

- **─→** : Sequência (próximo passo obrigatório)
- **├─** : Opção de caminho
- **┬─** : Múltiplas opções (alternativas)
- **└─** : Última opção
- **│** : Conexão vertical
- **✓** : Sucesso (fim do não-terminal)
- **ε** : Produção vazia (nada a processar)
- **Caixa com texto** : Não-terminal (outro gráfo)
- **Texto entre aspas** : Terminal (token)
- **Texto em MAIÚSCULAS** : Terminal (tipo de token)

## Fluxo de Análise

O parser segue o seguinte fluxo geral:

```
INICIO
   │
   ↓
programa ──→ esperado FUNCTION main ( )
   │
   ├──→ corpo ──→ declaracoes
   │            │
   │            └──→ comandos ──→ repetição até fechar }
   │
   ├──→ atribuicao → leitura → escrita
   │    condicional → repeticao → blocoInterno
   │
   ├──→ expressaoAritmetica
   │    │
   │    ├──→ termo ──→ fator (número, ID ou parênteses)
   │    │
   │    └──→ operadores aritméticos (+ -)
   │
   ├──→ expressaoRelacional
   │    │
   │    ├──→ termoRelacional (comparações)
   │    │
   │    └──→ operadores lógicos (&& ||)
   │
   └──→ Fim do programa
       │
       ✓ Sucesso ou ✗ Erro
```

## Conjuntos de Símbolos Sincronizadores

Para recuperação de erros:

- **Após declaração:** `;` ou `let`, `const`, `{`
- **Após comando:** `;` ou próximo comando ou `}`
- **Após expressão:** `;`, `)`, operador relacional
- **Após bloco:** `}`, `else`, `while`, ou EOF

Estes símbolos permitem ao parser recuperar-se de erros e continuar a análise.
