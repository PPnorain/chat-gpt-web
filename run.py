from config import Config
from lib.model import Model, Prompt, Conversation

if __name__=='__main__':
    conf = Config.conf
    tokenizer, model = Model.general_loading(conf.model_path, conf.model_name)
    Conversation.conversation(tokenizer, model)
    # Conversation.conversation_chat(tokenizer, model)