"""
pylox.loxcallfunction
~~~~~~~~~~~~~~~~
class LoxFunction that implements LoxCallable
"""
from pylox.loxcallable import LoxCallable
from pylox.environment import Environment
from pylox.error import Return


class LoxFunction(LoxCallable):
    """
    LoxFunction
    """
    def __init__(self, declaration=None, closure=None):
        """
        init
        :param declaration: declarations
        :param closure: closure
        """
        self._declaration = declaration
        self.closure = closure

    def arity(self):
        """
        returns arity
        :return: int
        """
        return len(self._declaration.params)

    def call(self, interpreter, arguments):
        """
        calls the arguemnt
        :param interpreter: environment/interpreter
        :param arguments: arguments
        :return: None
        """
        environment = Environment(self.closure)
        for i in range(len(arguments)):
            environment.define(self._declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self._declaration.body, environment)
        except Return as return_error:
            return return_error.value
        return None

    def __str__(self):
        """
        overrides string
        :return: str
        """
        return "<fn {}>".format(self._declaration.name.lexeme)
