from scanner import Scanner, TokenType


class TestScannerStatement:
    def test_statement(self):
        line = "var language = lox;"
        scanner = Scanner(line)
        scanner.scan_tokens()
        assert scanner._source == "var language = lox;"
        assert scanner.tokens[0].__dict__['lexeme'] == 'var'
        assert scanner.tokens[1].__dict__.get('lexeme') == 'language'
        assert scanner.tokens[2].__dict__.get('lexeme') == '='
        assert scanner.tokens[3].__dict__.get('lexeme') == 'lox'
        assert scanner.tokens[4].__dict__.get('lexeme') == ';'
        assert scanner.tokens[5].__dict__.get('lexeme') == ''


class TestScannerSingleChars:
    def test_parens(self):
        line = "()"
        scanner = Scanner(line)
        scanner.scan_tokens()
        assert scanner.tokens[0].__dict__['lexeme'] == '('
        assert scanner.tokens[0].__dict__['type'] == TokenType.LEFT_PAREN
        assert scanner.tokens[1].__dict__['lexeme'] == ')'
        assert scanner.tokens[1].__dict__['type'] == TokenType.RIGHT_PAREN

    def test_braces(self):
        line = "{}"
        scanner = Scanner(line)
        scanner.scan_tokens()
        print(scanner)
        assert scanner.tokens[0].__dict__['lexeme'] == '{'
        assert scanner.tokens[0].__dict__['type'] == TokenType.LEFT_BRACE
        assert scanner.tokens[1].__dict__['lexeme'] == '}'
        assert scanner.tokens[1].__dict__['type'] == TokenType.RIGHT_BRACE

    def test_comma(self):
        line = ","
        scanner = Scanner(line)
        scanner.scan_tokens()
        print(scanner)
        assert scanner.tokens[0].__dict__['lexeme'] == ','
        assert scanner.tokens[0].__dict__['type'] == TokenType.COMMA
        assert scanner.tokens[1].__dict__['lexeme'] == ''
        assert scanner.tokens[1].__dict__['type'] == TokenType.EOF

    def test_dot(self):
        line = "."
        scanner = Scanner(line)
        scanner.scan_tokens()
        print(scanner)
        assert scanner.tokens[0].__dict__['lexeme'] == '.'
        assert scanner.tokens[0].__dict__['type'] == TokenType.DOT
        assert scanner.tokens[1].__dict__['lexeme'] == ''
        assert scanner.tokens[1].__dict__['type'] == TokenType.EOF

    def test_minus(self):
        line = "-"
        scanner = Scanner(line)
        scanner.scan_tokens()
        print(scanner)
        assert scanner.tokens[0].__dict__['lexeme'] == '-'
        assert scanner.tokens[0].__dict__['type'] == TokenType.MINUS
        assert scanner.tokens[1].__dict__['lexeme'] == ''
        assert scanner.tokens[1].__dict__['type'] == TokenType.EOF

    def test_plus(self):
        line = "+"
        scanner = Scanner(line)
        scanner.scan_tokens()
        print(scanner)
        assert scanner.tokens[0].__dict__['lexeme'] == '+'
        assert scanner.tokens[0].__dict__['type'] == TokenType.PLUS
        assert scanner.tokens[1].__dict__['lexeme'] == ''
        assert scanner.tokens[1].__dict__['type'] == TokenType.EOF

    def test_semicolon(self):
        line = ';'
        scanner = Scanner(line)
        scanner.scan_tokens()
        assert scanner.tokens[0].__dict__['lexeme'] == ';'
        assert scanner.tokens[0].__dict__['type'] == TokenType.SEMICOLON
        assert scanner.tokens[1].__dict__['lexeme'] == ''
        assert scanner.tokens[1].__dict__['type'] == TokenType.EOF

    def test_slash(self):
        line = '/'
        scanner = Scanner(line)
        scanner.scan_tokens()
        assert scanner.tokens[0].__dict__['lexeme'] == '/'
        assert scanner.tokens[0].__dict__['type'] == TokenType.SLASH
        assert scanner.tokens[1].__dict__['lexeme'] == ''
        assert scanner.tokens[1].__dict__['type'] == TokenType.EOF

    def test_star(self):
        line = '*'
        scanner = Scanner(line)
        scanner.scan_tokens()
        assert scanner.tokens[0].__dict__['lexeme'] == '*'
        assert scanner.tokens[0].__dict__['type'] == TokenType.STAR
        assert scanner.tokens[1].__dict__['lexeme'] == ''
        assert scanner.tokens[1].__dict__['type'] == TokenType.EOF
