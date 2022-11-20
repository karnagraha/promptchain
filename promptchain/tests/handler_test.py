from promptchain import handler, service

def test_handler():
    h = handler.Handler(service.Loopback())
    r = h.handle(["input"])
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.output[0] == "input"

def test_prompt_handler():
    h = handler.PromptHandler("test")
    r = h.handle(["input"])
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.output[0] == "test"

def test_condition_handler():
    def fn(input, service_unused):
        return input == "input"
    h = handler.ConditionHandler(fn)
    r = h.handle(["input"])
    assert r.status == handler.HandlerStatus.SUCCESS_TRUE
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.output[0] == "input"

    r = h.handle(["not input"])
    assert r.status == handler.HandlerStatus.SUCCESS_FALSE
    assert r.status != handler.HandlerStatus.SUCCESS
    assert r.output[0] == "not input"

def test_classification_handler():
    classifications = {
        "cat1": ["input1", "input2"],
        "cat2": ["input3", "input4"],
    }
    h = handler.ClassificationHandler(classifications)
    r = h.handle(["input"])
    assert r.status == handler.HandlerStatus.SUCCESS_CLASSIFIED
    assert r.input[0] == "input"
    # can't really test the rest of these on loopback very well
    assert "cat1" in r.prompt[0]
    assert "cat2" in r.prompt[0]
    assert "input1" in r.prompt[0]
    assert "input2" in r.prompt[0]
    assert "input3" in r.prompt[0]
    assert "input4" in r.prompt[0]


def test_split_handler():
    h = handler.SplitHandler(r"\. *")
    r = h.handle(["input1. input2."])
    assert r.status == handler.HandlerStatus.SUCCESS
    assert len(r.input) == 1
    assert len(r.output) == 2
    assert r.output[0] == "input1"
    assert r.output[1] == "input2"

def test_join_handler():
    h = handler.JoinHandler(". ")
    r = h.handle(["input1", "input2"])
    assert r.status == handler.HandlerStatus.SUCCESS
    assert len(r.input) == 2
    assert len(r.output) == 1
    assert r.output[0] == "input1. input2"