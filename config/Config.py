from collections import namedtuple
MODEL_NAME = 'chatglm-6b'
model_dic = {
    'bloom':{
            'model_path':'/home/kemove/workspace/4.Model/bloom-560m',
            'model_name':'bloom',
        },
    'chatglm-6b':{
            'model_path':'/home/kemove/workspace/4.Model/chatglm-6b',
            'model_name':'chatglm',
    },
}
conf = {
    'model_path':model_dic[MODEL_NAME]['model_path'],
    'model_name':model_dic[MODEL_NAME]['model_name'],
}

Conf = namedtuple('Conf', conf.keys())
conf = Conf(**conf)
