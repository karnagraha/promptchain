import collections
from .handler import HandlerStatus


class Pipeline:
    """A pipeline is a DAG of handlers, where the output of one serves as the input for the next, based on the status of the previous handleresult."""
    def __init__(self):
        self.first = None
        self.handlers = {}
        self.outputs = collections.defaultdict(dict)

    
    def add_handler(self, handler, input=None, input_status=HandlerStatus.SUCCESS):
        name = handler.__class__.__name__ + str(len(self.handlers))

        if self.first is None:
            if input is not None:
                raise ValueError("Cannot specify input for first handler")
            self.first = name
        elif input is None:
            raise ValueError("Must specify input for non-first handler")
        else:
            self.outputs[input][input_status] = name
        self.handlers[name] = handler
        return name

    def handle(self, text):
        result = None
        handler_name = self.first
        while handler_name is not None:
            print(f"handling {text} with {handler_name}")
            handler = self.handlers[handler_name]
            outputs = self.outputs[handler_name]

            result = handler.handle(text)
            # set up next loop
            text = result.output
            try:
                handler_name = outputs[result.status]
            except KeyError:
                handler_name = None
        return result