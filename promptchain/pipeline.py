from promptchain.handler import HandlerStatus
class Pipeline:
    """A pipeline is an ordered collection of handlers, where the output of one serves as the input for the next."""
    def __init__(self):
        self.handlers = []
    
    def add_handler(self, handler):
        self.handlers.append(handler)

    def handle(self, text):
        result = None
        for handler in self.handlers:
            result = handler.handle(text)
            text = result.output
        return result