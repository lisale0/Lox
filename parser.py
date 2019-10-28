"""
Parser
~~~~~~~~~~~~~~~~
"""
import expr as Expr
import stmt as Stmt
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
        statements = []
        while not self._at_end():
            statements.append(self._declaration())
        return statements

    def _statement(self):
        if self._match(types=[TokenType.FOR]):
            return self._for_statement()
        if self._match(types=[TokenType.IF]):
            return self._if_statement()
        if self._match(types=[TokenType.PRINT]):
            return self._print_statement()
        if self._match(types=[TokenType.WHILE]):
            return self._while_statement()
        if self._match(types=[TokenType.LEFT_BRACE]):
            return Stmt.Block(self._block())

        return self._expression_statement()

    def _declaration(self):
        try:
            if self._match(types=[TokenType.VAR]):
                return self._var_declaration()
            return self._statement()
        except ParseError:
            self._synchronize()
            return None

    def _if_statement(self):
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after 'if' condition.")
        thenBranch = self._statement()
        elseBranch = None
        if self._match(types=[TokenType.ELSE]):
            elseBranch = self._statement()
        return Stmt.If(condition, thenBranch, elseBranch)

    def _print_statement(self):
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def _expression_statement(self):
        expr = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)

    def _block(self):
        statements = list()
        while not self._check(TokenType.RIGHT_BRACE) and not self._at_end():
            statements.append(self._declaration())
        self._consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def _assignment(self):
        expr = self._or()
        if self._match(types=[TokenType.EQUAL]):
            equals = self._previous()
            value = self._assignment()
            if isinstance(expr, Expr.Variable):
                name = expr.name
                return Expr.Assign(name, value)
            self._error(equals, "Invalid assignment target.")
        return expr

    def _or(self):
        expr = self._and()
        while self._match(types=[TokenType.OR]):
            operator = self._previous()
            right = self._and()
            expr = Expr.Logical(expr, operator, right)
        return expr

    def _and(self):
        expr = self._equality()
        while self._match(types=[TokenType.AND]):
            operator = self._previous()
            right = self._equality()
            expr = Expr.Logical(expr, operator, right)
        return expr

    def _expression(self):
        """ expression  """
        return self._assignment()

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
        if self._match(types=[TokenType.IDENTIFIER]):
            return Expr.Variable(self._previous())
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

    def _var_declaration(self):
        """
        variable declarations
        :return:
        """
        name = self._consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self._match(types=[TokenType.EQUAL]):
            initializer = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    def _while_statement(self):
        """
        parse while statements
        :return:
        """
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self._statement()
        return Stmt.While(condition, body)

    def _for_statement(self):
        """
        parse for statements
        :return:
        """
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        if self._match(types=[TokenType.SEMICOLON]):
            initializer = None
        elif self._match(types=[TokenType.VAR]):
            initializer = self._var_declaration()
        else:
            initializer = self._expression_statement()

        condition = None
        if not self._check(TokenType.SEMICOLON):
            condition = self._expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self._check(TokenType.RIGHT_PAREN):
            increment = self._expression()
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self._statement()

        if increment:
            body = Stmt.Block([body, Stmt.Expression(increment)])

        if condition is None:
            condition = Expr.Literal(True)

        body = Stmt.While(condition, body)

        if initializer:
            body = Stmt.Block([initializer, body])
        return body


class ParseError(Exception):
    """ return error """
