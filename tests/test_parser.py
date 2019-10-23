"""
test.test_parser
~~~~~~~~~~~~~~~~
Test file for parser
"""
from parser import Parser
from scanner import Scanner
import expr


class TestParser:
    """
    testing the parser
    """
    def test_add(self):
        """
        test addition
        :return: None
        """
        line = '3 + 4'
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        ast = Parser(tokens, "").parse()
        assert ast.left.value == 3
        assert ast.operator.lexeme == '+'
        assert ast.right.value == 4

    def test_sub(self):
        """
        test subtraction
        :return: None
        """
        line = '9 - 8'
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        ast = Parser(tokens, "").parse()
        assert ast.left.value == 9
        assert ast.operator.lexeme == '-'
        assert ast.right.value == 8

    def test_negative(self):
        """
        test negative number
        :return: None
        """
        line = '2 * -8'
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        ast = Parser(tokens, "").parse()
        assert ast.left.value == 2
        assert ast.operator.lexeme == '*'
        assert ast.right.operator.lexeme == '-'
        assert ast.right.right.value == 8

    def test_paren(self):
        """
        test paren
        :return: None
        """
        line = '2 * (5 + 8)'
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        ast = Parser(tokens, "").parse()
        assert ast.left.value == 2
        assert ast.operator.lexeme == '*'
        assert ast.right.__class__ == expr.Grouping
        assert ast.right.expression.left.value == 5
        assert ast.right.expression.operator.lexeme == '+'
        assert ast.right.expression.right.value == 8
