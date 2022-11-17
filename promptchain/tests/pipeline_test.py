from promptchain import pipeline, handler, service

def test_pipeline():
    p = pipeline.Pipeline()
    h = handler.Handler(service.Loopback())
    p.add_handler(h)
    r = p.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.input == "input"
    assert r.prompt == "input"
    assert r.output == "input"

def test_prompt_pipeline():
    p = pipeline.Pipeline()
    h = handler.PromptHandler("{} test", service.Loopback())
    p.add_handler(h)
    r = p.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.input == "input"
    assert r.prompt == "input test"
    assert r.output == "input test"

def test_multi_pipeline():
    p = pipeline.Pipeline()
    h = handler.Handler(service.Loopback())
    p.add_handler(h)
    p.add_handler(h)
    r = p.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.input == "input"
    assert r.prompt == "input"
    assert r.output == "input"

def test_condition_pipeline():
    p = pipeline.Pipeline()
    h = handler.ConditionHandler(lambda x: x == "input", service.Loopback())
    p.add_handler(h)
    r = p.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS_TRUE
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.input == "input"
    assert r.prompt == "input"
    assert r.output == "input"

    r = p.handle("not input")
    assert r.status == handler.HandlerStatus.SUCCESS_FALSE
    assert r.status != handler.HandlerStatus.SUCCESS
    assert r.input == "not input"
    assert r.prompt == "not input"
    assert r.output == "not input"