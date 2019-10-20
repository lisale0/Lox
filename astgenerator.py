#!/user/bin/env python3
"""
astgenerator
~~~~~~~~~~~~~~~~
generates AST written to expr.py
"""
tab = "    "

base_desc = {
    "Expr": {
        "Unary": [["scanner.Token", "operator"], ["Expr", "right"]],
        "Binary": [["Expr", "left"], ["scanner.Token", "operator"], ["Expr", "right"]],
        "Grouping" : [["Expr", "expression"]],
        "Literal" : [["object", "value"]],
        "Chain": [["Expr", "left"], ["Expr", "right"]],
    }
}


def begin(con):
    """
    write to the beginning of expr.py
    :param con: connection/file to write to
    :return: None
    """
    con.write("# GENERATED FILE - DO NOT MANUALLY EDIT!\n")
    con.write("# Generated by astgenerator.py\n")
    con.write("from abc import ABC, abstractmethod\n\n\n")


def define_visitor(con):
    """
    create the visitor class
    :param con: connection/file to write to
    :return: None
    """
    visitors = ["visit_binary_expr", "visit_grouping_expr",
                "visit_literal_expr", "visit_unary_expr"]
    visitor_def = [tab + "@abstractmethod" + tab + "\n" + tab + "def "\
                   + visitor + "(self):\n" + tab + tab + "pass\n\n" \
                   for visitor in visitors]
    con.write("class Visitor(ABC):\n")
    con.writelines(visitor_def)
    con.write("\n")


def define_ast(con, base_name, types):
    """
    create the Expr abstract method
    :param con: connection/file to write to
    :param base_name: base/parent class name
    :param types: the types to create
    :return: None
    """
    con.writelines(["class " + base_name + "(ABC):\n" + tab,
                    "@abstractmethod\n" + tab,
                    "def accept(self, visitor):\n",
                    tab + tab,
                    "pass\n\n\n"])
    for expr_type, expr in types.items():
        define_type(con, base_name, expr_type, expr)


def define_type(con, base_name, class_name, fields):
    """
    create the methods
    :param con: connection/file to write to
    :param base_name: base/parent class name
    :param class_name: class name
    :param fields: the fields associated to the method
    :return: None
    """
    _, names = zip(*fields)
    field_str = ", ".join(names)
    con.writelines("class {0}({1}):\n".format(class_name, base_name) +
                   tab +
                   "def __init__(self, {0}):".format(field_str))
    init_stmts = [tab + tab + "self." + name + " = " + name + "\n" for name in names]
    con.write("\n")
    con.writelines(init_stmts)
    con.write("\n")
    con.writelines([tab + "def accept(self, visitor):\n",
                    tab + tab + "return visitor.visit_"
                    + class_name.lower() + "_expr" + "(self)\n\n\n"])


if __name__ == "__main__":
    path = "expr.py"
    with open(path, "w+") as f:
        begin(f)
        define_visitor(f)
        define_ast(f, "Expr", base_desc["Expr"])
