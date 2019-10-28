"""
lox.scanner
~~~~~~~~~~~~~~~~
handles lexing
"""
from enum import Enum, auto


class TokenType(Enum):
    """ Token types"""
    # assign automatic values
    # Single-character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens.
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals.
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords.
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


class Token:
    """ Token class"""
    def __init__(self, token_type, lexeme, literal, line):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return "{0} {1} {2}".format(self.type, self.lexeme, self.literal)


class Scanner:
    """ Scanner class"""
    def __init__(self, source):
        self.error = None
        self.tokens = []
        self._start = 0
        self._current = 0
        self._line = 1
        self._source = source

        self._keywords = {
            "print": TokenType.PRINT,
            "var": TokenType.VAR,
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "fun": TokenType.FUN,
            "for": TokenType.FOR,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "while": TokenType.WHILE
        }

    def _at_end(self):
        """
        check if end
        :return: (boolean) if end
        """
        return self._current >= len(self._source)

    def _scan_token(self):
        """
        scans tokens
        :return: None
        """
        c = self._advance()
        if c == '(':
            self._add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self._add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self._add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self._add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self._add_token(TokenType.COMMA)
        elif c == '.':
            self._add_token(TokenType.DOT)
        elif c == '-':
            self._add_token(TokenType.MINUS)
        elif c == '+':
            self._add_token(TokenType.PLUS)
        elif c == ';':
            self._add_token(TokenType.SEMICOLON)
        elif c == '*':
            self._add_token(TokenType.STAR)

        # operators
        elif c == '!':
            self._add_token(TokenType.BANG_EQUAL if self._match('=') else TokenType.BANG)
        elif c == '=':
            self._add_token(TokenType.EQUAL_EQUAL if self._match('=') else TokenType.EQUAL)
        elif c == '<':
            self._add_token(TokenType.LESS_EQUAL if self._match('=') else TokenType.LESS)
        elif c == '>':
            self._add_token(TokenType.GREATER_EQUAL if self._match('=') else TokenType.GREATER)
        elif c == '/':
            if self._match('/'):
                while self._peek() != '\n' and not self._at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif c in {' ', '\r', '\t'}:
            pass
        elif c == '\n':
            self._line += 1

        # string literal
        elif c == '"':
            self._string()

        # number
        elif c.isdigit():
            self._number()
        elif c == 'o':
            if self._peek() == 'r':
                self._add_token(TokenType.OR)
        elif c.isalpha():
            self._identifier()
        else:
            self.error(self._line, "unexpected character: {}".format(c))

    def _add_token(self, token_type, literal=None):
        """
        adds token to self.tokens
        :param type: the type
        :param literal: literbal
        :return: None
        """
        text = self._source[self._start:self._current]
        self.tokens.append(Token(token_type, text, literal, self._line))

    def _advance(self):
        """
        advance position in self._source
        :return: next position in source
        """
        self._current += 1
        return self._source[self._current - 1]

    def _match(self, expected):
        """
        find whether there is a match
        :param expected: the expected match
        :return: (boolean)
        """
        if self._at_end():
            return False
        if self._source[self._current] != expected:
            return False
        self._current += 1
        return True

    def _peek(self):
        """
        peek at the next char/token
        :return: next position in source
        """
        if self._at_end():
            return '\0'
        else:
            return self._source[self._current]

    def _string(self):
        """
        gets the string lexeme
        :return: (string)
        """
        while self._peek() != '"' and not self._at_end():
            if self._peek() == '\n':
                self._line += 1
            self._advance()
        if self._at_end():
            self.error = "{0} Unterminated string.".format(self._line)
            return

            # advance to find "
        self._advance()

        # trim the surrounding quotes
        value = self._source[self._start + 1: self._current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self):
        """
        get the number if a digit is detected and add to token
        :return:
        """
        while self._peek().isdigit():
            self._advance()
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()
        self._add_token(TokenType.NUMBER, float(self._source[self._start:self._current]))

    def _peek_next(self):
        """
        peek_next
        :return: (string)
        """
        if self._current + 1 > len(self._source):
            return '/0'
        return self._source[self._current + 1]

    def _identifier(self):
        """
        identifier
        :return:
        """
        while self._peek().isalnum():
            self._advance()
        if self._source[self._start:self._current] in self._keywords:
            key = self._source[self._start:self._current]
            reserved_type = self._keywords[key]
            self._add_token(reserved_type)
        else:
            self._add_token(TokenType.IDENTIFIER)

    def scan_tokens(self):
        """
        scan tokens calling _scan_token
        :return:
        """
        while not self._at_end():
            self._start = self._current
            self._scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self._source))
        return self.tokens
