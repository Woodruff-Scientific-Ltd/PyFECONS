import pyfecons


class TemplateException(Exception):
    """General template exception."""

    def __init__(self, message):
        self.message = message
        # pyfecons.logger.error(message) # if logger added
        super().__init__(self.message)
