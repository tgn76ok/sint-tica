"""
Test Suite - Testes para o compilador
"""

import sys
import os

# Adiciona o diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lexer import Lexer
from src.parser import Parser, SyntaxError


def test_lexer_basico():
    """Testa análise léxica básica"""
    codigo = "function main() { let x: number; }"
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()

    assert len(tokens) > 0
    assert tokens[0].tipo == "FUNCTION"
    assert tokens[1].tipo == "MAIN"
    print("✓ test_lexer_basico passou")


def test_parser_declaracao_simples():
    """Testa parsing de declaração simples"""
    codigo = "function main() { let x: number; }"
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        parser.parse()
        print("✓ test_parser_declaracao_simples passou")
    except SyntaxError as e:
        print(f"✗ test_parser_declaracao_simples falhou: {e}")
        return False

    return True


def test_parser_atribuicao():
    """Testa parsing de atribuição"""
    codigo = "function main() { let x: number; x = 5; }"
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        parser.parse()
        print("✓ test_parser_atribuicao passou")
    except SyntaxError as e:
        print(f"✗ test_parser_atribuicao falhou: {e}")
        return False

    return True


def test_parser_expressao_aritmetica():
    """Testa parsing de expressão aritmética com precedência"""
    codigo = "function main() { let x: number; x = 2 + 3 * 4; }"
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        parser.parse()
        print("✓ test_parser_expressao_aritmetica passou")
    except SyntaxError as e:
        print(f"✗ test_parser_expressao_aritmetica falhou: {e}")
        return False

    return True


def test_parser_condicional():
    """Testa parsing de estrutura condicional"""
    codigo = """function main() { 
        let x: number; 
        if (x > 0) { 
            console.log("positivo"); 
        } else { 
            console.log("negativo"); 
        } 
    }"""
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        parser.parse()
        print("✓ test_parser_condicional passou")
    except SyntaxError as e:
        print(f"✗ test_parser_condicional falhou: {e}")
        return False

    return True


def test_parser_repeticao():
    """Testa parsing de estrutura de repetição"""
    codigo = """function main() { 
        let x: number; 
        while (x < 10) { 
            x = x + 1; 
        } 
    }"""
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        parser.parse()
        print("✓ test_parser_repeticao passou")
    except SyntaxError as e:
        print(f"✗ test_parser_repeticao falhou: {e}")
        return False

    return True


def test_parser_bloco_interno():
    """Testa parsing de bloco interno"""
    codigo = """function main() { 
        let x: number; 
        { 
            x = 5; 
            { 
                x = x + 1; 
            } 
        } 
    }"""
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        parser.parse()
        print("✓ test_parser_bloco_interno passou")
    except SyntaxError as e:
        print(f"✗ test_parser_bloco_interno falhou: {e}")
        return False

    return True


def test_parser_erro_falta_ponto_virgula():
    """Testa detecção de erro: falta de ponto e vírgula"""
    codigo = "function main() { let x: number }"
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        parser.parse()
        print("✗ test_parser_erro_falta_ponto_virgula falhou: erro não foi detectado")
        return False
    except SyntaxError as e:
        print(f"✓ test_parser_erro_falta_ponto_virgula passou (erro detectado)")
        return True


def test_parser_erro_tipo_invalido():
    """Testa detecção de erro: tipo inválido"""
    codigo = "function main() { let x: integer; }"
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        parser.parse()
        print("✗ test_parser_erro_tipo_invalido falhou: erro não foi detectado")
        return False
    except SyntaxError as e:
        print(f"✓ test_parser_erro_tipo_invalido passou (erro detectado)")
        return True


def test_parser_leitura_escrita():
    """Testa parsing de read e console.log"""
    codigo = """function main() { 
        let x: number; 
        read(x); 
        console.log(x); 
    }"""
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        parser.parse()
        print("✓ test_parser_leitura_escrita passou")
    except SyntaxError as e:
        print(f"✗ test_parser_leitura_escrita falhou: {e}")
        return False

    return True


def test_parser_expressao_relacional():
    """Testa parsing de expressão relacional"""
    codigo = """function main() { 
        let x: number; 
        let y: number; 
        if (x > 0 && y < 10 || x == 5) { 
            console.log("ok"); 
        } 
    }"""
    lexer = Lexer(codigo)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        parser.parse()
        print("✓ test_parser_expressao_relacional passou")
    except SyntaxError as e:
        print(f"✗ test_parser_expressao_relacional falhou: {e}")
        return False

    return True


if __name__ == '__main__':
    print("="*60)
    print("Suite de Testes - Mini Compiler")
    print("="*60)
    print()

    testes = [
        test_lexer_basico,
        test_parser_declaracao_simples,
        test_parser_atribuicao,
        test_parser_expressao_aritmetica,
        test_parser_condicional,
        test_parser_repeticao,
        test_parser_bloco_interno,
        test_parser_erro_falta_ponto_virgula,
        test_parser_erro_tipo_invalido,
        test_parser_leitura_escrita,
        test_parser_expressao_relacional,
    ]

    passed = 0
    failed = 0

    for teste in testes:
        try:
            resultado = teste()
            if resultado is not False:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {teste.__name__} falhou com exceção: {e}")
            failed += 1

    print()
    print("="*60)
    print(f"Resultados: {passed} passou(ram), {failed} falhou(falharam)")
    print("="*60)
