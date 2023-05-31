

def make_prompt(question, prompt=None):
    if prompt:
        return prompt.format_map({'instruction':question})
    return question