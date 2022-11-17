import re

from enum import Enum

class HandlerResult:
    def __init__(self, status, input, prompt, output):
        self.status = status
        self.input = input
        self.prompt = prompt
        self.output = output

    def __str__(self):
        return self.output
    
    def __bool__(self):
        return self.status == HandlerStatus.SUCCESS

class HandlerStatus(Enum):
    FAILURE = 0
    SUCCESS = 1
    SUCCESS_TRUE = 1
    SUCCESS_FALSE = 2


class Handler:
    """Basic handler that converts input to output via service."""
    def __init__(self, service):
        self.service = service

    def get_prompt(self, input):
        return input

    def handle(self, input):
        prompt = self.get_prompt(input)
        output = self.service.call(prompt)
        result = HandlerResult(HandlerStatus.SUCCESS, input, prompt, output)
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

    def handle(self, input):
        condition_fn = self.condition
        return condition_fn(input, self.service)