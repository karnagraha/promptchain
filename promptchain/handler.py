import re


class Handler:
    """Basic handler that converts input to output via service."""
    def __init__(self, service):
        """Initialize the handler with a result preprocessor."""
        self.service = service

    def get_prompt(self, input):
        return input

    def handle(self, input):
        prompt = self.get_prompt(input)
        output = self.service.call(prompt)
        return output


class PromptHandler(Handler):
    """Basic handler that formats a provided string template"""
    def __init__(self, prompt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = prompt

    def get_prompt(self, input):
        return self.prompt.format(input)

class ConditionHandler(Handler):
    """Functions like an if statement, returns true or false."""
    def __init__(self, condition, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.condition = condition

    def handle(self, input):
        condition_fn = self.condition
        return condition_fn(input)
