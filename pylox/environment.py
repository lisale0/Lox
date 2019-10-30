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
        self._enclosing = enclosing

    def define(self, name, value):
        """
        :param name: variable name
        :param value: value of var
        :return: None
        """
        self.values[name] = value

    def get(self, name):
        """
        return value
        :param name: key
        :return: str
        """
        if self.values.get(name.lexeme) is not None:
            return self.values[name.lexeme]

        if self._enclosing:
            return self._enclosing.values.get(name.lexeme)
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
        if self._enclosing:
            key = name.lexeme
            self._enclosing.values[str(key)] = value
            return
        raise LoxRuntimeError(name, "Undefined variable {0}.".format(name.lexeme))
