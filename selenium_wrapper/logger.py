class Logger:
    def __init__(self, logger):
        self.wrapped = logger

    def format_msg(self, verb, msg):
        if not verb.endswith(':'):
            verb += ':'
        return f'{verb:7}{msg}'

    def debug(self, verb, msg):
        self.wrapped.debug(self.format_msg(verb, msg))

    def info(self, verb, msg):
        self.wrapped.info(self.format_msg(verb, msg))

    def warn(self, verb, msg):
        self.wrapped.warn(self.format_msg(verb, msg))

    def error(self, verb, msg):
        self.wrapped.error(self.format_msg(verb, msg))

    def fatal(self, verb, msg):
        self.wrapped.fatal(self.format_msg(verb, msg))
