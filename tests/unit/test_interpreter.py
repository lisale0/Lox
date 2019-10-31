"""
test.test_interpreter
~~~~~~~~~~~~~~~~
Test file for interpreter
"""

from pylox.scanner import Scanner
from pylox.parser import Parser
from pylox.interpreter import Interpreter


class TestInterpreter:
    def test_var(self):
        line = 'var beverage = "espresso";\nprint beverage;'
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, "")
        statements = parser.parse();
        Interpreter().interpret(statements)
