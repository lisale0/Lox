"""
Parser
~~~~~~~~~~~~~~~~
"""
import expr as Expr
from scanner import TokenType


class Parser:
    """
    Parser class
    """
    def __init__(self, tokens, set_error):
        self._current = 0
        self.tokens = tokens
        self.error_handler = set_error

    def parse(self):
        """
        parse
        :return: expressions
        """
        try:
            return self._expression()
        except ParseError:
            return None

    def _expression(self):
        """ expression  """
        return self._equality()

    def _equality(self):
        """
        expands to the equality rule
        equality → comparison ( ( "!=" | "==" ) comparison )* ;
        :return:
        """
        expr = self._comparison()
        while self._match(types=[TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self._previous()
            right = self._comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def _comparison(self):
        """
        operator   → "==" | "!=" | "<" | "<=" | ">" | ">="
        :return:
        """
        expr = self._addition()
        while self._match(types=[TokenType.GREATER, TokenType.GREATER_EQUAL,
                                 TokenType.LESS, TokenType.LESS_EQUAL]):
            operator = self._previous()
            right = self._addition()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def _match(self, types):
        """
        checks to see if the current token is any of the given types
        :param types:
        :return: boolean
        """
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _previous(self):
        """ get previous """
        return self.tokens[self._current - 1]

    def _advance(self):
        """
        consumes the current token and returns it
        :return: token
        """
        if not self._at_end():
            self._current += 1
        return self._previous()


    def _check(self, token_type):
        """
        check if the current token is of the given type
        :param token_type:
        :return: boolean
        """
        if self._at_end():
            return False
        return self._peek().type == token_type

    def _at_end(self):
        """
        checks if there are anymore tokens
        :return: boolean
        """
        return self._peek().type == TokenType.EOF

    def _peek(self):
        """
        returns the current token we have yet to consume and previous()
        :return: token
        """
        return self.tokens[self._current]

    def _previous(self):
        """
        returns the previous token we have consumed
        :return: token
        """
        return self.tokens[self._current - 1]

    def _addition(self):
        """
        comparison → addition ( ( ">" | ">=" | "<" | "<=" ) addition )* ;
        :return: expression
        """
        expr = self._multiplication()
        while self._match(types=(TokenType.MINUS, TokenType.PLUS)):
            operator = self._previous()
            right = self._multiplication()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def _multiplication(self):
        """
        multiplication
        :return: expression
        """
        expr = self._unary()
        while self._match(types=[TokenType.SLASH, TokenType.STAR]):
            operator = self._previous()
            right = self._unary()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def _unary(self):
        """
        unary → ( "!" | "-" ) unary | primary ;
        :return: expression
        """
        if self._match(types=[TokenType.BANG, TokenType.MINUS]):
            operator = self._previous()
            right = self._unary()
            return Expr.Unary(operator, right)
        return self._primary()

    def _primary(self):
        """
        primary → NUMBER | STRING | "false" | "true" | "nil"
        | "(" expression ")" ;
        :return: expression
        """
        if self._match(types=[TokenType.FALSE]):
            return Expr.Literal(False)
        if self._match(types=[TokenType.TRUE]):
            return Expr.Literal(True)
        if self._match(types=[TokenType.NIL]):
            return Expr.Literal(None)
        if self._match(types=[TokenType.NUMBER, TokenType.STRING]):
            return Expr.Literal(self._previous().literal)
        if self._match(types=[TokenType.LEFT_PAREN]):
            expr = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        raise self._error(self._peek(), "Expect expression.")

    def _consume(self, token_type, message):
        """
        checks to see if the next token is of the expected type
        :param token_type: token type
        :param message: message
        :return: error
        """
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _error(self, token_type, message):
        """
        set error
        :param token_type:
        :param message:
        :return: error
        """
        self.error_handler(token_type, message)
        return ParseError()

    def _synchronize(self):
        """
        synchronize the tokens
        :return: None
        """
        self._advance()
        while not self._at_end():
            if self._previous().type == TokenType.SEMICOLON:
                return

            tokens = [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN
            ]
            if self._peek().type in tokens:
                return
            self._advance()


class ParseError(Exception):
    """ return error """
