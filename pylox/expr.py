# GENERATED FILE - DO NOT MANUALLY EDIT!
# Generated by astgenerator.py
from abc import ABC, abstractmethod


class Visitor(ABC):
    @abstractmethod    
    def visit_binary_expr(self):
        pass

    @abstractmethod    
    def visit_grouping_expr(self):
        pass

    @abstractmethod    
    def visit_literal_expr(self):
        pass

    @abstractmethod    
    def visit_unary_expr(self):
        pass

    @abstractmethod    
    def visit_assign_expr(self):
        pass

    @abstractmethod    
    def visit_expression_stmt(self):
        pass

    @abstractmethod    
    def visit_print_stmt(self):
        pass

    @abstractmethod    
    def visit_var_stmt(self):
        pass

    @abstractmethod    
    def visit_block_stmt(self):
        pass

    @abstractmethod    
    def visit_variable_expr(self):
        pass

    @abstractmethod    
    def visit_if_stmt(self):
        pass

    @abstractmethod    
    def visit_logical_expr(self):
        pass

    @abstractmethod    
    def visit_while_stmt(self):
        pass


# ExprVisitor
class Expr(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary_expr(self)


class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visit_assign_expr(self)


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary_expr(self)


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal_expr(self)


class Logical(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical_expr(self)


class Chain(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def accept(self, visitor):
        return visitor.visit_chain_expr(self)


class Variable(Expr):
    def __init__(self, name):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable_expr(self)

