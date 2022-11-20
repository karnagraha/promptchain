import re

from enum import Enum

class HandlerResult:
    # prompt and output are lists to allow for handlers with multiple outputs
    def __init__(self, status, input, prompts, outputs):
        self.status = status
        self.input = input
        self.prompt = prompts
        self.output = outputs


class HandlerStatus(Enum):
    FAILURE = 0
    SUCCESS = 1
    SUCCESS_TRUE = 1
    SUCCESS_FALSE = 2
    SUCCESS_CLASSIFIED = 3

class Handler:
    """Base handler class that converts input to output via service. Not very useful on its own."""
    def __init__(self, service):
        self.service = service

    def get_prompt(self, input):
        return input

    def handle(self, inputs):
        prompts = []
        outputs = []
        for input in inputs:
            prompt = self.get_prompt(input)
            output = self.service.call(prompt)
            prompts.append(prompt)
            outputs.append(output)
            result = HandlerResult(HandlerStatus.SUCCESS, inputs, prompts, outputs)
        return result


class PromptHandler(Handler):
    """Basic handler that formats a provided string template"""
    def __init__(self, prompt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = prompt

    def get_prompt(self, input):
        return self.prompt.format(input)


class ConditionHandler(Handler):
    """Calls custom code in handler.  Must return a HandlerResult object."""
    def __init__(self, condition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.condition = condition

    def handle(self, inputs):
        if len(inputs) != 1:
            raise ValueError("ConditionHandler can only handle one input at a time")

        condition_fn = self.condition
        if condition_fn(inputs[0], self.service):
            return HandlerResult(HandlerStatus.SUCCESS_TRUE, inputs, inputs, inputs)
        return HandlerResult(HandlerStatus.SUCCESS_FALSE, inputs, inputs, inputs)

class ClassificationHandler(Handler):
    def __init__(self, classifications, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.classifications = classifications

    def get_prompt(self, input):
        prompt = "Classify the following text:\n\n"
        for classification, examples in self.classifications.items():
            for example in examples:
                prompt = prompt + "TEXT: " + example + "\nCLASS: " + classification + "\n\n"
        prompt = prompt + "TEXT: " + input + "\nCLASS:"
        return prompt

    def handle(self, inputs):
        if len(inputs) != 1:
            raise ValueError("ClassificationHandler can only handle one input at a time")

        prompt = self.get_prompt(inputs[0])
        output = self.service.call(prompt)
        return HandlerResult(HandlerStatus.SUCCESS_CLASSIFIED, inputs, [prompt], [output])

class SplitHandler(Handler):
    """SplitHandler will attempt to separate lists of items into individual items."""
    def __init__(self, separator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.separator = separator
    
    def handle(self, inputs):
        if len(inputs) != 1:
            raise ValueError("SplitHandler can only handle one input at a time")

        prompts = inputs
        outputs = re.split(self.separator, inputs[0])
        print(outputs)
        # get rid of a trailing empty string
        if outputs[-1] == "":
            outputs = outputs[:-1]
        return HandlerResult(HandlerStatus.SUCCESS, inputs, prompts, outputs)

class JoinHandler(Handler):
    """Take multiple inputs and return a single input."""
    def __init__(self, separator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.separator = separator
    
    def handle(self, inputs):
        output = self.separator.join(inputs)
        return HandlerResult(HandlerStatus.SUCCESS, inputs, [output], [output])
