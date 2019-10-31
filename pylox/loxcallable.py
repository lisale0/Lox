"""
pylox.loxcallable
~~~~~~~~~~~~~~~~
abstract class LoxCallable
"""
from abc import ABC, abstractmethod


class LoxCallable(ABC):
    """
    abstract class LoxCallable
    """
    @abstractmethod
    def arity(self):
        """
        checks arity
        """

    @abstractmethod
    def call(self):
        """
        calls the function
        """
