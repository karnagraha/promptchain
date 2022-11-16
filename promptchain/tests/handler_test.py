from promptchain import handler, service

def test_handler():
    s = service.Loopback()
    h = handler.Handler(s)
    assert h.handle("input") == "input"

def test_prompt_handler():
    s = service.Loopback()
    h = handler.PromptHandler("test", s)
    assert h.handle("input") == "test"
