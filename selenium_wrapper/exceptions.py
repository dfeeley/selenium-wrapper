class WrappedException(Exception):
    def __init__(self, message, underlying):
        self.message = message
        self.underlying = underlying

    def __str__(self):
        return self.message
