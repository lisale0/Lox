"""
Interpreter
~~~~~~~~~~~~~~~~
"""
from expr import Visitor
from scanner import TokenType


class Interpreter(Visitor):
    """
    interpreter class
    """
    def interpret(self, expression):
        """
        called by lox to interpret expression
        :param expression: expression
        :return: None
        """
        try:
            value = self._evaluate(expression)
            return value
        except LoxRuntimeError as error:
            LoxRuntimeError(message=error)

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

    def _evaluate(self, expr):
        """
        evaluate the expressions
        :param expr: expression
        :return:
        """
        return expr.accept(self)

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


class LoxRuntimeError(RuntimeError):
    """
    Lox Runtime Error
    """
    def __init__(self, token=None, message=None):
        RuntimeError.__init__(message)
        self.token = token
