from promptchain import pipeline, handler, service

def test_pipeline():
    p = pipeline.Pipeline()
    h = handler.Handler(service.Loopback())
    p.add_handler(h)
    assert p.handle("input") == "input"

def test_prompt_pipeline():
    p = pipeline.Pipeline()
    h = handler.PromptHandler("test", service.Loopback())
    p.add_handler(h)
    assert p.handle("input") == "test"

def test_multi_pipeline():
    p = pipeline.Pipeline()
    h = handler.Handler(service.Loopback())
    p.add_handler(h)
    p.add_handler(h)
    assert p.handle("input") == "input"

def test_condition_pipeline():
    p = pipeline.Pipeline()
    h = handler.ConditionHandler(lambda x: x == "input", service.Loopback())
    p.add_handler(h)
    assert p.handle("input") == True
    assert p.handle("not input") == False


