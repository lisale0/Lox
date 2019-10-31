#!/usr/bin/env python3
"""
lox.lox
~~~~~~~~~~~~~~~~
The main file for the lox programming language interpreter
"""
import sys
from pylox.parser import Parser
from pylox.interpreter import Interpreter
from pylox.resolver import Resolver
from pylox.scanner import Scanner


class Lox:
    """ Lox class"""
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        self.interpreter = Interpreter()

    def run_file(self, file):
        """ Runs file
        :param file: input file
        """
        with open(file) as content:
            program = content.read()

        self.run(program)
        if self.had_error:
            sys.exit(65)
        elif self.had_runtime_error:
            sys.exit(70)

    def run_prompt(self):
        """ Runs prompt """
        print("Running prompt")
        while True:
            line = input(">> ")
            self.run(line)
            # If we had an error, we should reset at new prompt
            self.had_error = False
            self.had_runtime_error = False

    def run(self, line):
        """ Runs the input
        :param line: line to tokenize and eval
        """
        scanner = Scanner(line)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens, self.error)
        statements = parser.parse()
        resolver = Resolver(self.interpreter)
        resolver.resolve(statements)
        self.interpreter.interpret(statements)
        if self.had_error:
            return

    def error(self, line, message):
        """ error
        :param line: the location of error
        :param message: error message
        """
        self.report(line + " " + message)

    def runtimeerror(self, error):
        """
        set runtimeerror message
        :param error: error message
        :return: None
        """
        error_message = "{0} \n [line {1}]".format(error.get_message(), error.token.line)
        print(error_message)
        self.had_runtime_error = True

    def report(self, line, where=None, message=None):
        """ error
        :param line: line of error
        :param where: location of error
        :param: message: error message
        """
        self.had_error = True
        raise Exception("[Line {0}] Error {1}: {2} ".format(line, where, message))


def main():
    """ Main """
    lox = Lox()
    print(sys.argv)
    if len(sys.argv) > 2:
        print("Usage: jlox [script]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        lox.run_file(sys.argv[1])
    else:
        lox.run_prompt()


if __name__ == "__main__":
    main()
