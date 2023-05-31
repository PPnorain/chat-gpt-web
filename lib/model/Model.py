from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModel
from peft import PeftConfig, PeftModel

class AutoModelWrapper:
    model_map = {
        'bloom':AutoModelForCausalLM,
        'chatglm':AutoModel,
    }
    @classmethod
    def from_pretrained(self, model_path, model_name, lora_path=None):
        model = self.model_map[model_name].from_pretrained(model_path, trust_remote_code=True)
        if lora_path is not None:
            model = PeftModel.from_pretrained(model, lora_path)
        return model

def general_loading(model_path, model_name, lora_path=None):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelWrapper.from_pretrained(model_path, model_name, lora_path).half().cuda()
    return tokenizer, model

# ---------------- 2. chatGLM-single -----------------
# def Ptuning_loading():
#     model_path = config.Config.LLM_PATH
#     checkpoint_path = config.Config.LLM_ADAPTOR_PATH

#     tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
#     conf = AutoConfig.from_pretrained(model_path, trust_remote_code=True, pre_seq_len=128)
#     model = AutoModel.from_pretrained(model_path, config=conf, trust_remote_code=True)
#     prefix_state_dict = torch.load(os.path.join(checkpoint_path, "pytorch_model.bin"))
#     new_prefix_state_dict = {}
#     for k, v in prefix_state_dict.items():
#         if k.startswith("transformer.prefix_encoder."):
#             new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
#     model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)

#     # Comment out the following line if you don't use quantization
#     model = model.quantize(4)
#     model = model.half().cuda()
#     model.transformer.prefix_encoder.float()
#     model = model.eval()
#     return tokenizer, model
