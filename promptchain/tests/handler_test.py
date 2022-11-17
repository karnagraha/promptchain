from promptchain import handler, service

def test_handler():
    s = service.Loopback()
    h = handler.Handler(s)
    r = h.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.output == "input"

def test_prompt_handler():
    s = service.Loopback()
    h = handler.PromptHandler("test", s)
    r = h.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.output == "test"

def test_condition_handler():
    s = service.Loopback()
    h = handler.ConditionHandler(lambda x: x == "input", s)
    r = h.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS_TRUE
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.output == "input"

    r = h.handle("not input")
    assert r.status == handler.HandlerStatus.SUCCESS_FALSE
    assert r.status != handler.HandlerStatus.SUCCESS
    assert r.output == "not input"