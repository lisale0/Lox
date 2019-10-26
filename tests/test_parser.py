"""
test.test_parser
~~~~~~~~~~~~~~~~
Test file for parser
"""
from parser import Parser
from scanner import Scanner
import expr
import stmt


class TestExpressions:
    """
    testing the parser
    """
    def test_add(self):
        """
        test addition
        :return: None
        """
        line = '3 + 4;'
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        ast = Parser(tokens, "").parse()
        print(ast)
        assert isinstance(ast[0], stmt.Expression)
        assert ast[0].expression.left.value == 3
        assert ast[0].expression.operator.lexeme == '+'
        assert ast[0].expression.right.value == 4

    def test_sub(self):
        """
        test subtraction
        :return: None
        """
        line = '9 - 8;'
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        ast = Parser(tokens, "").parse()
        assert ast[0].expression.left.value == 9
        assert ast[0].expression.operator.lexeme == '-'
        assert ast[0].expression.right.value == 8

    def test_negative(self):
        """
        test negative number
        :return: None
        """
        line = '2 * -8;'
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        ast = Parser(tokens, "").parse()
        print(ast)
        assert ast[0].expression.left.value == 2
        assert ast[0].expression.operator.lexeme == '*'
        assert ast[0].expression.right.operator.lexeme == '-'
        assert ast[0].expression.right.right.value == 8

    def test_paren(self):
        """
        test paren
        :return: None
        """
        line = '2 * (5 + 8);'
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        ast = Parser(tokens, "").parse()
        assert ast[0].expression.left.value == 2
        assert ast[0].expression.operator.lexeme == '*'
        assert ast[0].expression.right.__class__ == expr.Grouping
        assert ast[0].expression.right.expression.left.value == 5
        assert ast[0].expression.right.expression.operator.lexeme == '+'
        assert ast[0].expression.right.expression.right.value == 8
