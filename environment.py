"""
Environment
~~~~~~~~~~~~~~~~
"""
class Environment:
    """
    Environment
    """
    def __init__(self, values=None, enclosing=None):
        self.values = values
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
        if self.values[name.lexeme]:
            return self.values[name.lexeme]

        if self._enclosing is not None:
            return self._enclosing[name]

        raise RuntimeError(message="Undefined variable '" + name.lexeme + "'.")

    def assign(self, name, value):
        """
        assign a new value to to values
        :param name: key
        :param value: val
        :return: None
        """
        if self.values[name.lexeme]:
            self.values[name.lexeme] = value
            return
        raise RuntimeError(message="Undefined variable '" + name.lexeme + "'.")
