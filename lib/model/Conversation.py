from . import Prompt
from config.Config import conf

def conversation(tokenizer, model):
    question = input("You:")
    while question != 'q':
        prompt = Prompt.make_prompt(question, prompt=conf.prompt)
        input_ids = tokenizer(prompt, return_tensors='pt')['input_ids'].cuda()
        output = model.generate(input_ids, max_length=512, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
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

def chatstream_api(question, history, tokenizer, model, prompt=None):
    # print('[Stream Chat]:', prompt, history)
    prompt = Prompt.make_prompt(question, prompt)
    print('prompt',prompt)
    for response, history in model.stream_chat(tokenizer, prompt, history):
        # print(response)
        yield response
    print(response, history)

def conversation_api(question, history, tokenizer, model, prompt=None):
    prompt = Prompt.make_prompt(question, prompt)
    print('prompt',prompt)
    input_ids = tokenizer(prompt, return_tensors='pt')['input_ids'].cuda()
    output = model.generate(input_ids=input_ids, max_length=512, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print(generated_text)
    return generated_text