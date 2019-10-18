"""
lox.lox
~~~~~~~~~~~~~~~~
The main file for the lox programming language interpreter
"""
import sys
from scanner import Scanner


class Lox:
    """ Lox class"""
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

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
    @staticmethod
    def run(line):
        """ Runs the input
        :param line: line to tokenize and eval
        """
        scanner = Scanner(line)
        scanner.scan_tokens()
        #list tokens here, loop through token and print them out

    def error(self, line, message):
        """ error
        :param line: the location of error
        :param message: error message
        """
        self.report(line + " " + message)

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
        lox.run_file(sys.argv[0])
    else:
        lox.run_prompt()


if __name__ == "__main__":
    main()
