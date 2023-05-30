from . import Prompt

def conversation(tokenizer, model):
    question = input("You:")
    while question != 'q':
        prompt = Prompt.make_prompt(question)
        input_ids = tokenizer(prompt, return_tensors='pt')['input_ids'].cuda()
        output = model.generate(input_ids, max_length=50, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        print(generated_text)
        question = input("You:")

def conversation_chat(tokenizer, model):
    model = model.eval()
    history = []
    question = input('You:')
    while question != 'q':
        response, history = model.chat(tokenizer, question, history=history)
        print(response)
        question = input('You:')

def chatstream_api(prompt, history, tokenizer, model):
    # print('[Stream Chat]:', prompt, history)
    for response, history in model.stream_chat(tokenizer, prompt, history):
        # print(response)
        yield response
    print(response)
