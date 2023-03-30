import openai
import config
openai.api_key = config.DevelopmentConfig.OPENAI_KEY


def generateChatResponse(prompt):
    messages = []
    messages.append({"role": "system", "content": "Your name is Hu. You are a helpful assistant."})
    question = {'role':'user', 'content':prompt}
    messages.append(question)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)

    try:
        answer = response['choices'][0]['message']['content'].replace('\n', '<br>')
    except:
        answer = 'Oops you beat the AI, try a different question, if the problem persists, come bacl later.'

    return answer
