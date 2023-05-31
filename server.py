from flask import Flask, render_template, jsonify, request
from flask_session import Session
import json, torch, os
from lib.weblib import web_backend
from lib.model import Conversation, Model
from config.Config import model_dic, prompt_path

app = Flask(__name__,static_folder='web/static/')
Session(app)
app.register_error_handler(404, web_backend.page_not_found)
app.template_folder = './web/templates'
app.config['tokenizer'] = app.config['model'] = None

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        tokenizer, model = app.config['tokenizer'], app.config['model']
        data = request.get_json()
        model_type, conversation_method = data.get('model'), data.get('conversation')
        print(model_type, conversation_method)
        question, history = data.get('prompt'), json.loads(data.get('history'))
        res = {}
        if conversation_method == '非流式对话':
            return app.response_class(Conversation.conversation_api(question, history, tokenizer, model, app.config.get('prompt', '')), mimetype='text/plain')        
        else:
            return app.response_class(Conversation.chatstream_api(question, history, tokenizer, model, app.config.get('prompt', '')), mimetype='text/plain')        
    return render_template('index.html', **locals())

@app.route('/model-selection', methods = ['POST', 'GET'])
def model_selection():
    if request.method == 'POST':
        model_type = request.get_json().get('model_type')
        app.config['tokenizer'] = app.config['model'] = None
        torch.cuda.empty_cache()
        print(model_type, model_dic.keys())
        if model_type not in model_dic.keys():
            return jsonify('failed'), 500
        app.config['tokenizer'], app.config['model'] = \
                Model.general_loading(model_dic[model_type]['model_path'], model_dic[model_type]['model_name'])
        print(model_type)
        return jsonify('ok'), 200

@app.route('/prompt-file', methods = ['POST', 'GET'])
def get_file_list():
    file_list = os.listdir(os.path.dirname(prompt_path))
    return jsonify(file_list), 200

@app.route('/prompt-selected', methods = ['POST', 'GET'])
def prompt_selected():
    if request.method == 'POST':
        prompt_selected = request.get_json().get('prompt_value')
        if prompt_selected == '': 
            app.config['prompt']= ''
            return jsonify('ok'), 200
        dirname = os.path.dirname(prompt_path)
        with open(os.path.join(dirname, prompt_selected), 'r') as f:
            app.config['prompt'] = f.read()
        print(app.config['prompt'])
        return jsonify('ok'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True, use_reloader=False)