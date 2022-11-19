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
        handler_name = self.first
        while handler_name is not None:
            result = self.handlers[handler_name].handle(text)

            next_handler_key = result.status
            # in the case of classification, the handler is specififed by the result output.
            if result.status == HandlerStatus.FAILURE:
                return None
            elif result.status == HandlerStatus.SUCCESS_CLASSIFIED:
                # In the case of a ClassificationHandler the next handler is identified by the Result Output
                # There should only be one output from a ClassificationHandler
                next_handler_key = result.output[0]
            else:
                # Otherwise update text for next query.
                # TODO: This needs to be changed when handlers with multiple outputs are supported.
                text = result.output[0]

            # Find the next handler in the chain
            try:
                handler_name = self.outputs[handler_name][next_handler_key]
            except KeyError:
                # TODO: add logging
                handler_name = None
        return result