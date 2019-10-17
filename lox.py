import sys
from scanner import Scanner

class Lox():
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def run_file(self, file):
        with open(file) as f:
            content = f.read()

        self.run(content)
        if self.had_error:
            sys.exit(65)
        elif self.had_runtime_error:
            sys.exit(70)

    def run_prompt(self):
        print("Running prompt")
        while True:
            line = input(">> ")
            self.run(line)
            # If we had an error, we should reset at new prompt
            self.had_error = False
            self.had_runtime_error = False

    def run(self, line):
        scanner = Scanner(line)
        scanner.scan_tokens()
        #list tokens here, loop through token and print them out

    def error(self, line, message):
        self.report(line + " " + message)

    def report(self, line, where, message):
        self.had_error = True
        raise Exception("[Line {0}] Error {1}: {2} ", line, where, message)


def main():
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
