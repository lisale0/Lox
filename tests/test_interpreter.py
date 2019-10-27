"""
test.test_interpreter
~~~~~~~~~~~~~~~~
Test file for interpreter
"""

from scanner import TokenType, Token, Scanner
from parser import Parser
from interpreter import Interpreter

class TestInterpreter:
    def test_var(self):
        line = 'var beverage = "espresso";\nprint beverage;'
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, "")
        statements = parser.parse();
        Interpreter().interpret(statements)



