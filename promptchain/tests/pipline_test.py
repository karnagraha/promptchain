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