"""
Interpreter
~~~~~~~~~~~~~~~~
"""
import time
from pylox.expr import Visitor
from pylox.scanner import TokenType
from pylox.environment import Environment
from pylox.error import LoxRuntimeError
from pylox.error import Return as ReturnError
from pylox.loxcallable import LoxCallable
from pylox.loxfunction import LoxFunction


class Interpreter(Visitor, LoxCallable):
    """
    interpreter class
    """
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.locals = []

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

    def _evaluate(self, expr):
        """
        evaluate the expressions
        :param expr: expression
        :return:
        """
        return expr.accept(self)

    def execute_block(self, statements, environment):
        """
        execute block statements
        :param statements: statement
        :param environment: environment
        :return: None
        """
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self._execute(statement)
        finally:
            self.environment = previous

    def _execute(self, stmt):
        """
        execute statement
        :param stmt: statement
        :return:
        """
        stmt.accept(self)

    def resolve(self, expr, depth):
        self.locals[expr] = depth

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

    def visit_variable_expr(self, expr):
        return self._lookup_variable(expr.name, expr)

    def _lookup_variable(self, name, expr):
        if expr in self.locals:
            distance = self.locals[expr]
        if not distance:
            return self.environment.getAt(distance, name.lexeme)

    def visit_assign_expr(self, expr):
        value = self._evaluate(expr.value)
        distance = self.locals[expr]
        if distance:
            self.environment.assignAt(distance, expr.name, value)
        else:
            self.globals[expr.name] = value
        return value

    def visit_logical_expr(self, expr):
        left = self._evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self._is_truthy(left):
                return left
        else:
            if self._is_truthy(left):
                return left
        return self._evaluate(expr.right)

    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(enclosing=self.environment))

    def visit_if_stmt(self, stmt):
        if self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self._execute(stmt.else_branch)

    def visit_while_stmt(self, stmt):
        while self._is_truthy(self._evaluate(stmt.condition)):
            self._execute(stmt.body)

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self._evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)

    def visit_expression_stmt(self, stmt):
        self._evaluate(stmt.expression)

    def visit_function_stmt(self, stmt):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)

    def visit_print_stmt(self, stmt):
        value = self._evaluate(stmt.expression)
        print(self._stringify(value))

    def visit_return_stmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self._evaluate(stmt.value)
        raise ReturnError(value)

    def visit_call_expr(self, expr):
        callee = self._evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self._evaluate(argument))
        if not isinstance(callee, LoxCallable):
            raise LoxRuntimeError(expr.paren, "Can only call functions and classes.")
        function = callee
        # check arity
        if len(arguments) is not function.arity():
            error_msg = "Expected {} arguments, but got {}."\
                .format(function.arity(), len(arguments))
            raise LoxRuntimeError(expr.paren, error_msg)
        return function.call(self, arguments)

    def arity(self):
        return 0

    def call(self):
        return time.time()

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
