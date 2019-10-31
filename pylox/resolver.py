"""
Resolver
~~~~~~~~~~~~
"""
from enum import Enum, auto
from pylox.expr import Visitor


class Resolver(Visitor):
    """
    resolver class
    """
    def __init__(self, interpreter):
        self._interpreter = interpreter
        self._current_function = FunctionType.NONE
        self.scopes = []

    def visit_block_stmt(self, stmt):
        self._begin_scope()
        self.resolve(stmt.statements)
        self._end_scope()

    def visit_var_stmt(self, stmt):
        self._declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self._define(stmt.name)

    def visit_variable_expr(self, expr):
        # if len(self.scopes) > 0 and self.scopes[-1][expr.name.lexeme] is False:
        #     self.error_handler.error(expr.name,
        #                              "Cannot read local variable in its own initializer.")
        self._resolve_local(expr, expr.name)

    def visit_assign_expr(self, expr):
        self.resolve(expr.value)
        self._resolve_local(expr, expr.name)

    def visit_function_stmt(self, stmt):
        self._declare(stmt.name)
        self._define(stmt.name)
        self._resolve_function(stmt, FunctionType.FUNCTION)

    def visit_expression_stmt(self, stmt):
        self.resolve(stmt.expression)

    def visit_if_stmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch:
            self.resolve(stmt.else_branch)

    def visit_print_stmt(self, stmt):
        self.resolve(stmt.expression)

    def visit_return_stmt(self, stmt):
        if self._current_function is FunctionType.NONE:
            self.error_handler.error(stmt.keyword, "Cannot return from top-level code.")
        if stmt.value:
            self.resolve(stmt.value)

    def visit_while_stmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visit_binary_expr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_call_expr(self, expr):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)

    def visit_grouping_expr(self, expr):
        self.resolve(expr.expression)

    def visit_literal_expr(self, expr):
        pass

    def visit_logical_expr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_unary_expr(self, expr):
        self.resolve(expr.right)

    def resolve(self, stmt):
        """
        resolving statements
        :param stmt: statement
        :return:
        """
        if isinstance(stmt, list):
            for statement in stmt:
                self.resolve(statement)
        else:
            stmt.accept(self)

    def _begin_scope(self):
        self.scopes.append({})

    def _end_scope(self):
        self.scopes.pop()

    def _declare(self, name):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.error_handler.error(name,
                                     "Variable with this name already declared in this scope.")
        if name.lexeme in self.scopes:
            self.error_handler.error(name,
                                     "Variable with this name already declared in this scope.")
        scope[name.lexeme] = False

    def _define(self, name):
        if len(self.scopes) == 0:
            return
        self.scopes[-1][name.lexeme] = True

    def _resolve_local(self, expr, name):
        for i in range(len(self.scopes)-1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self._interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def _resolve_function(self, function, function_type):
        enclosing_function = self._current_function
        self._current_function = function_type
        self._begin_scope()
        for param in function.params:
            self._declare(param)
            self._define(param)
        self.resolve(function.body)
        self._end_scope()
        self._current_function = enclosing_function


class FunctionType(Enum):
    """
    FunctionType
    """
    NONE = auto()
    FUNCTION = auto()
