#!/user/bin/env python3
"""
prettyprint
~~~~~~~~~~~~~~~~
"""
from expr import Visitor
import expr as Expr
from scanner import TokenType, Token


class ASTPrinter(Visitor):
    """
    Astprinter
    """
    def visit_binary_expr(self, expr):
        """
        visitor implementation of binary expr
        :param expr: expression
        :return: str
        """
        return self.parenthesize(expr.operator.lexeme, exprs=[expr.left, expr.right])

    def visit_grouping_expr(self, expr):
        """
        visitor implementation of grouping expr
        :param expr: expression
        :return: str
        """
        return self.parenthesize("group", exprs=[expr.expression])

    def visit_literal_expr(self, expr):
        """
        visitor implementation of literal expr
        :param expr: expression
        :return: str
        """
        if expr.value is None:
            return None
        return str(expr.value)

    def visit_unary_expr(self, expr):
        """
        visitor implementation of unary expr
        :param expr: expression
        :return: str
        """
        return self.parenthesize(expr.operator.lexeme, exprs=[expr.right])

    def visit_assign_expr(self):
        pass

    def visit_block_stmt(self):
        pass

    def visit_expression_stmt(self):
        pass

    def visit_print_stmt(self):
        pass

    def visit_var_stmt(self):
        pass

    def parenthesize(self, name, exprs):
        """
        parenthesize the expressions
        :param name: name
        :param exprs: the expression
        :return: str
        """
        str_arr = list()
        str_arr.append("(")
        str_arr.append(name)
        for expr in exprs:
            str_arr.append(" ")
            str_arr.append(expr.accept(self))
        str_arr.append(")")
        return " ".join(str_arr)

    def print_ast(self, expr):
        """
        print the ast
        :param expr: expression
        :return: str
        """
        return expr.accept(self)


if __name__ == "__main__":
    expression = Expr.Binary(
        Expr.Unary(
            Token(TokenType.MINUS, '-', None, 1),
            Expr.Literal(123)),
        Token(TokenType.STAR, "*", None, 1),
        Expr.Grouping(
            Expr.Literal(45.67)
        )
    )
    print(ASTPrinter().print_ast(expression))
