class Pipeline:
    """A pipeline is an ordered collection of handlers, where the output of one serves as the input for the next."""
    def __init__(self):
        self.handlers = []
    
    def add_handler(self, handler):
        self.handlers.append(handler)

    def handle(self, input):
        output = None

        for handler in self.handlers:
            output = handler.handle(input)
            if output is None or output is False:
                break
            elif output is True:
                continue
            # setup loop for next execution
            input = output
        return output
