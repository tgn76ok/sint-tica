"""
Main - Ponto de entrada do compilador
"""

import sys
import os
from src.lexer import Lexer
from src.parser import Parser, SyntaxError


def compile_file(filepath):
    """Compila um arquivo"""
    print(f"{'='*60}")
    print(f"Compilador MiniLanguage")
    print(f"{'='*60}")
    print(f"\nArquivo: {filepath}")

    try:
        # 1. Leitura do arquivo
        with open(filepath, 'r', encoding='utf-8') as f:
            codigo_fonte = f.read()

        print(f"✓ Arquivo lido com sucesso ({len(codigo_fonte)} caracteres)")

        # 2. Análise Léxica
        print(f"\n--- Fase 1: Análise Léxica ---")
        lexer = Lexer(codigo_fonte)
        tokens = lexer.tokenize()

        print(f"✓ Análise léxica concluída")
        print(f"  Total de tokens: {len(tokens)}")

        # Exibe alguns tokens (primeiros 10)
        print(f"\n  Primeiros tokens:")
        for i, token in enumerate(tokens[:10]):
            print(f"    {i+1}. {token}")
        if len(tokens) > 10:
            print(f"    ... ({len(tokens)-10} tokens adicionais)")

        # 3. Análise Sintática
        print(f"\n--- Fase 2: Análise Sintática ---")
        cont = 0
        for token in tokens:
            if token.tipo == "LPAREN":
                cont += 1
                print(f"Token {token.valor} encontrado:", token)
            if token.tipo == "RPAREN":
                cont -= 1
                
                print(f"Token {token.valor} encontrado:", token)
            if token.tipo == "MOD":
                print(f"Token {token.valor} encontrado:", token)
            if token.tipo == "EQ":
                print(f"Token {token.valor} encontrado:", token)
                   
                
        print("Contador final de parênteses:", cont)
        parser = Parser(tokens)
        parser.parse()

        print(f"✓ Análise sintática concluída com sucesso!")
        print(f"\n{'='*60}")
        print(f"✓ Compilação bem-sucedida!")
        print(f"{'='*60}\n")

        return True

    except FileNotFoundError:
        print(f"✗ Erro: Arquivo '{filepath}' não encontrado")
        return False

    except SyntaxError as e:
        print(f"✗ {e}")
        return False

    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    if len(sys.argv) > 1:
        arquivo = sys.argv[1]
    else:
        arquivo = "tests/programa_ckp2_sexta.mc"

    if compile_file(arquivo):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
