from promptchain import pipeline, handler, service

def test_pipeline():
    p = pipeline.Pipeline()
    h = handler.Handler(service.Loopback())
    p.add_handler(h)
    r = p.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.input == "input"
    assert r.prompt[0] == "input"
    assert r.output[0] == "input"

def test_prompt_pipeline():
    p = pipeline.Pipeline()
    h = handler.PromptHandler("{} test", service.Loopback())
    p.add_handler(h)
    r = p.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.input == "input"
    assert r.prompt[0] == "input test"
    assert r.output[0] == "input test"


def test_condition_pipeline():
    p = pipeline.Pipeline()
    def fn(input, service_unused):
        if input == "input":
            return handler.HandlerResult(handler.HandlerStatus.SUCCESS_TRUE, input, input, input)
        else:
            return handler.HandlerResult(handler.HandlerStatus.SUCCESS_FALSE, input, input, input)

    h = handler.ConditionHandler(fn, service.Loopback())
    p.add_handler(h)
    r = p.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS_TRUE
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.input == "input"
    assert r.prompt[0] == "input"
    assert r.output[0] == "input"

    r = p.handle("not input")
    assert r.status == handler.HandlerStatus.SUCCESS_FALSE
    assert r.status != handler.HandlerStatus.SUCCESS
    assert r.input == "not input"
    assert r.prompt[0] == "not input"
    assert r.output[0] == "not input"


def test_multi_pipeline():
    p = pipeline.Pipeline()
    s = service.Loopback()
    def fn(input, service_unused):
        if input == "input":
            return handler.HandlerResult(handler.HandlerStatus.SUCCESS_TRUE, input, input, input)
        else:
            return handler.HandlerResult(handler.HandlerStatus.SUCCESS_FALSE, input, input, input)
    h = handler.ConditionHandler(fn, s)
    name = p.add_handler(h)

    # set a downstream result for each result from the condition handler
    h2 = handler.PromptHandler("{} success", s)
    name2 = p.add_handler(h2, name, handler.HandlerStatus.SUCCESS_TRUE)
    h3 = handler.PromptHandler("{} fail", s)
    name3 = p.add_handler(h3, name, handler.HandlerStatus.SUCCESS_FALSE)


    r = p.handle("input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.input == "input"
    assert r.prompt[0] == "input success"
    assert r.output[0] == "input success"

    r = p.handle("not input")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.input == "not input"
    assert r.prompt[0] == "not input fail"
    assert r.output[0] == "not input fail"


def test_classification_pipeline():
    p = pipeline.Pipeline()
    # It's difficult to test this without an actualy LLM

    # classification will use a static handler to classify the input to the first category
    h = handler.ClassificationHandler({
        "category1": ["input1", "input2"],
        "category2": ["input3", "input4"],
    }, service.Static("category1"))
    name = p.add_handler(h)

    # set a downstream result for each result from the condition handler
    h2 = handler.PromptHandler("{} success", service.Loopback())
    p.add_handler(h2, name, "category1")
    h3 = handler.PromptHandler("{} fail", service.Loopback())
    p.add_handler(h3, name, "category2")

    r = p.handle("input1")
    assert r.status == handler.HandlerStatus.SUCCESS
    assert r.input == "input1"
    assert r.prompt[0] == "input1 success"
    assert r.output[0] == "input1 success"







