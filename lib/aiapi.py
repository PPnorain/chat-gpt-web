import torch, os
from lib.model import Model
from 

tokenizer, model = Model.general_loading()


# tokenizer, model = General_loading()
# tokenizer, model = Ptuning_loading()
# model_path = './ChatGLM'

# ---------------- 2.1 chatGLM-single -----------------
def ChatGLM_ChatResponse(prompt, history):
    # history = [('你是谁？','我的名字叫Hai，是一个有用的人工智能助手，可以帮助回答用户的各种问题。')]
    print(prompt, history)
    answer, history = model.chat(tokenizer, prompt, history)
    return answer



# ---------------- 3. 虚拟测试api -----------------
def persudoChatResponse(prompt):
    answer = 'received!'
    return answer
