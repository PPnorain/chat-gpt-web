from collections import namedtuple
MODEL_NAME = 'chatglm-6b'
model_dic = {
    'bloom-560m':{
            'model_path':'/home/kemove/workspace/4.Model/bloom-560m',
            'model_name':'bloom',
        },
    'bloom-560m-lora':{
            'model_path':'/home/kemove/workspace/4.Model/bloom-560m',
            'model_name':'bloom',
            'lora_path':'',
        },
    'chatglm-6b':{
            'model_path':'/home/kemove/workspace/4.Model/chatglm-6b',
            'model_name':'chatglm',
    },
}
prompt_path='/home/kemove/workspace/5.Program/model_platform/config/prompt/instruction.txt'
with open(prompt_path, 'r') as f:
    prompt = f.read()
conf = {
    'model_path':model_dic[MODEL_NAME]['model_path'],
    'model_name':model_dic[MODEL_NAME]['model_name'],
    'lora_path':model_dic[MODEL_NAME].get('lora_path', None),
    'prompt':prompt,
}

Conf = namedtuple('Conf', conf.keys())
conf = Conf(**conf)
