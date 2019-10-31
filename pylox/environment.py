"""
Environment
~~~~~~~~~~~~~~~~
"""
from pylox.error import LoxRuntimeError


class Environment:
    """
    Environment
    """
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        """
        :param name: variable name
        :param value: value of var
        :return: None
        """
        self.values[name] = value

    def ancestor(self, distance):
        """
        ancestor walks the chain of enclosing environments
        :param distance:
        :return:
        """
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

    def getAt(self, distance, name):
        """
        get at
        :param distance: distance
        :param name: name
        :return:
        """
        return self.ancestor(distance).values[name]

    def assignAt(self, distance, name, value):
        """
        assign
        :param distance:
        :param name:
        :param value:
        :return:
        """
        self.ancestor(distance).values[name.lexeme] = value

    def get(self, name):
        """
        return value
        :param name: key
        :return: str
        """
        if self.values.get(name.lexeme) is not None:
            return self.values[name.lexeme]

        if self.enclosing:
            return self.enclosing.values.get(name.lexeme)
        raise LoxRuntimeError(name, "Undefined variable {0}.".format(name.lexeme))

    def assign(self, name, value):
        """
        assign a new value to to values
        :param name: key
        :param value: val
        :return: None
        """
        if self.values.get(name.lexeme):
            self.values[name.lexeme] = value
            return
        if self.enclosing:
            key = name.lexeme
            self.enclosing.values[str(key)] = value
            return
        raise LoxRuntimeError(name, "Undefined variable {0}.".format(name.lexeme))
