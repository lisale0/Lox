"""
Errors
~~~~~~~~~~~~~~~~
"""


class LoxRuntimeError(RuntimeError):
    """
    Lox Runtime Error
    """
    def __init__(self, token=None, message=None):
        self.token = token
        self.message = message

    def __str__(self):
        return "{}\n[line {}]".format(self.message, self.token.line)


class Return(RuntimeError):
    """
    Return
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "return error: {}".format(self.value)
