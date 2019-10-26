"""
test.test_interpreter
~~~~~~~~~~~~~~~~
Test file for interpreter
"""

from scanner import TokenType, Token
from expr import Binary, Literal
from stmt import Expression
from interpreter import Interpreter


class TestInterpreter:
    def test_add(self):
        expression = Expression("3 + 4;")
        val = Interpreter().interpret([expression])
        print(val)
        assert val == 7.0

    def test_sub(self):
        token = Token(TokenType.MINUS, '-', None, '3 - 4;')
        expression = Binary(Literal(3.0), token, Literal(4.0))
        val = Interpreter().interpret(expression)
        assert val == -1

    def test_mul(self):
        token = Token(TokenType.STAR, '*', None, '2 * 3;')
        expression = Binary(Literal(2.0), token, Literal(3.0))
        val = Interpreter().interpret(expression)
        assert val == 6

    def test_slash(self):
        token = Token(TokenType.SLASH, '/', None, '9 * 3;')
        expression = Binary(Literal(9.0), token, Literal(3.0))
        val = Interpreter().interpret(expression)
        assert val == 3

    def test_greater_true(self):
        token = Token(TokenType.GREATER, '>', None, '9 > 3')
        expression = Binary(Literal(9.0), token, Literal(3.0))
        val = Interpreter().interpret(expression)
        assert val is True

    def test_greater_false(self):
        token = Token(TokenType.GREATER, '>', None, '2 > 3')
        expression = Binary(Literal(2.0), token, Literal(3.0))
        val = Interpreter().interpret(expression)
        assert val is False

    def test_greater_equal_true(self):
        token = Token(TokenType.GREATER_EQUAL, '>', None, '9 >= 9')
        expression = Binary(Literal(9.0), token, Literal(9.0))
        val = Interpreter().interpret(expression)
        assert val is True

    def test_greater_equal_false(self):
        token = Token(TokenType.GREATER_EQUAL, '>', None, '2 >= 3')
        expression = Binary(Literal(2.0), token, Literal(3.0))
        val = Interpreter().interpret(expression)
        assert val is False

    def test_less_true(self):
        token = Token(TokenType.LESS, '<', None, '3 < 9')
        expression = Binary(Literal(3.0), token, Literal(9.0))
        val = Interpreter().interpret(expression)
        assert val is True

    def test_less_false(self):
        token = Token(TokenType.LESS, '>', None, '2 < 1')
        expression = Binary(Literal(2.0), token, Literal(2.0))
        val = Interpreter().interpret(expression)
        assert val is False

    def test_less_equal_true(self):
        token = Token(TokenType.LESS_EQUAL, '>', None, '9 <= 9')
        expression = Binary(Literal(9.0), token, Literal(9.0))
        val = Interpreter().interpret(expression)
        assert val is True

    def test_less_equal_false(self):
        token = Token(TokenType.LESS_EQUAL, '>', None, '2 <= 1')
        expression = Binary(Literal(2.0), token, Literal(1.0))
        val = Interpreter().interpret(expression)
        assert val is False

    def test_bang_equal(self):
        token = Token(TokenType.BANG_EQUAL, '!=', None, '32!= 1')
        expression = Binary(Literal(32.0), token, Literal(1.0))
        val = Interpreter().interpret(expression)
        assert val is True

    def test_bang_equal_false(self):
        token = Token(TokenType.BANG_EQUAL, '!=', None, '1 != 1')
        expression = Binary(Literal(1.0), token, Literal(1.0))
        val = Interpreter().interpret(expression)
        assert val is False

    def test_equal_equal(self):
        token = Token(TokenType.EQUAL_EQUAL, '==', None, '32 == 32')
        expression = Binary(Literal(32.0), token, Literal(32.0))
        val = Interpreter().interpret(expression)
        assert val is True

    def test_equal_equal_false(self):
        token = Token(TokenType.EQUAL_EQUAL, '==', None, '32 == 30')
        expression = Binary(Literal(32.0), token, Literal(30.0))
        val = Interpreter().interpret(expression)
        assert val is False
