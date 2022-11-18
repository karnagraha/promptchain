from promptchain import handler, service

def test_handler():
    h = handler.Handler(service.Loopback())
    r = h.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.output == "input"

def test_prompt_handler():
    h = handler.PromptHandler("test", service.Loopback())
    r = h.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.output == "test"

def test_condition_handler():
    def fn(input, service_unused):
        if input == "input":
            return handler.HandlerResult(handler.HandlerStatus.SUCCESS_TRUE, input, input, input)
        else:
            return handler.HandlerResult(handler.HandlerStatus.SUCCESS_FALSE, input, input, input)
    h = handler.ConditionHandler(fn, service.Loopback())
    r = h.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS_TRUE
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.output == "input"

    r = h.handle("not input")
    assert r.status == handler.HandlerStatus.SUCCESS_FALSE
    assert r.status != handler.HandlerStatus.SUCCESS
    assert r.output == "not input"

def test_classification_handler():
    classifications = {
        "cat1": ["input1", "input2"],
        "cat2": ["input3", "input4"],
    }
    h = handler.ClassificationHandler(classifications, service.Loopback())
    r = h.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS_CLASSIFIED
    assert r.input == "input"
    # can't really test the rest of these on loopback very well
    assert "cat1" in r.prompt 
    assert "cat2" in r.prompt
    assert "input1" in r.prompt
    assert "input2" in r.prompt
    assert "input3" in r.prompt
    assert "input4" in r.prompt