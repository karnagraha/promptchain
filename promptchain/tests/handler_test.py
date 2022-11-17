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