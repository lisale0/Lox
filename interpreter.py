"""
Interpreter
~~~~~~~~~~~~~~~~
"""
from expr import Visitor
from scanner import TokenType
from environment import Environment
from error import LoxRuntimeError


class Interpreter(Visitor):
    """
    interpreter class
    """
    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements):
        """
        called by lox to interpret expression
        :param statements: statements
        :return: None
        """
        try:
            for statement in statements:
                self._execute(statement)
        except RuntimeError as error:
            raise Exception(error)

    def visit_binary_expr(self, expr):
        """
        binary expression
        :param expr: expr
        :return:
        """
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)
        op_type = expr.operator.type

        if op_type == TokenType.GREATER:
            self._check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        elif op_type == TokenType.GREATER_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        elif op_type == TokenType.LESS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        elif op_type == TokenType.LESS_EQUAL:
            self._check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        elif op_type == TokenType.MINUS:
            self._check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        elif op_type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
        elif op_type == TokenType.SLASH:
            self._check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        elif op_type == TokenType.STAR:
            self._check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        elif op_type == TokenType.BANG_EQUAL:
            return not self._is_equal(left, right)
        elif op_type == TokenType.EQUAL_EQUAL:
            return self._is_equal(left, right)
        else:
            return None
        return None

    def visit_grouping_expr(self, expr):
        """
        group expressions
        :param expr: expression
        :return:
        """
        return self._evaluate(expr.expression)

    def visit_literal_expr(self, expr):
        """
        literal expressions
        :param expr: expression
        :return:
        """
        return expr.value

    def visit_unary_expr(self, expr):
        """
        unary expressions
        :param expr: expressions
        :return:
        """
        right = self._evaluate(expr.right)
        op_type = expr.operator.type
        if op_type == TokenType.MINUS:
            return -float(right)
        elif op_type == TokenType.BANG:
            return not self._is_truthy(right)
        else:
            return None

    def visit_expression_stmt(self, stmt):
        self._evaluate(stmt.expression)

    def visit_print_stmt(self, stmt):
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_assign_expr(self, expr):
        value = self._evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_block_stmt(self, stmt):
        self._execute_block(stmt.statements, Environment(enclosing=self.environment))

    def visit_if_stmt(self, stmt):
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)

    def visit_logical_expr(self, expr):
        left = self._evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if self._is_truthy(left):
                return left
        return self._evaluate(expr.right)

    def visit_while_stmt(self, stmt):
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)

    def _evaluate(self, expr):
        """
        evaluate the expressions
        :param expr: expression
        :return:
        """
        return expr.accept(self)

    def _execute(self, stmt):
        stmt.accept(self)

    def _execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self.environment = previous

    @staticmethod
    def _is_truthy(object):
        """
        evaluate true/false of an object
        :param object: object
        :return:
        """
        if object is None:
            return False
        if isinstance(object, bool):
            return bool(object)
        return True

    @staticmethod
    def _is_equal(left, right):
        """
        test equality
        :param left: left
        :param right: right
        :return: bool
        """
        if left is None and right is None:
            return True
        if left is None:
            return False
        return left == right

    @staticmethod
    def _check_number_operands(operator, left, right):
        """
        check operands
        :param operator: operator
        :param left: left value
        :param right: right value
        :return: None/runtimeerror
        """
        if isinstance(left, float) and isinstance(right, float):
            return
        raise LoxRuntimeError(operator, "Operands must be numbers.")

    @staticmethod
    def _stringify(object):
        """
        returns string of an object
        :param object: object
        :return: str
        """
        if object is None:
            if isinstance(object, float):
                text = str(object)
                if text[-2:] == '.0':
                    text = text[:-2]
                return text
        return str(object)
