from flask import Flask, render_template, jsonify, request
from flask_session import Session
import json
from lib.weblib import web_backend
from lib.model import Conversation, Model
from config.Config import conf

app = Flask(__name__,static_folder='web/static/')
Session(app)
app.register_error_handler(404, web_backend.page_not_found)
app.template_folder = '/home/kemove/workspace/5.Program/model_platform/web/templates'

tokenizer, model = Model.general_loading(conf.model_path, conf.model_name)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        prompt, history = data.get('prompt'), json.loads(data.get('history'))
        res = {}
        print(f'prompt:{prompt}, history:{history}')
        return app.response_class(Conversation.chatstream_api(prompt, history, tokenizer, model), mimetype='text/plain')        
    return render_template('index.html', **locals())

# @app.route('/test/', methods = ['POST', 'GET'])
# def test():
#     if request.method == 'POST':
#         prompt = request.form['prompt']
#         # history = json.loads(request.form['history'])
#         # history = json.loads(request.form.get('history'))
#         history = json.loads(request.form.get('history'))
#         res = {}
#         # res['answer'] = aiapi.generateChatResponse(prompt)
#         # res['answer'] = aiapi.persudoChatResponse(prompt)
#         print(f'prompt:{prompt}, history:{history}')
#         res['answer'] = aiapi.ChatGLM_ChatResponse(prompt, history)
#         return jsonify(res), 200
#     return render_template('test.html', **locals())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True, use_reloader=False)