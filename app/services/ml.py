def response(data, model=None):
    if model is None:
        output = "Я пока не очень умный, но очень скоро смогу разговаривать"
    else:
        output = model.process(data)
    return output
