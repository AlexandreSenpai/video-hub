from flask import Flask, render_template, request, redirect, session
from utils.download_file import Upload
from utils.storage_utils import Storage
from utils.tk_generator import id_gen
from datetime import datetime
from utils.firebase_utils import firebase
import os

app = Flask(__name__, template_folder='./pages/')
stor = Storage()
upload = Upload()
db = firebase()

@app.route('/', methods=['GET'])
def main_page():
    log_msg = session['upload_log'] if 'upload_log' in session.keys() else None
    print(log_msg)
    videos = db.limit_videos(48)
    recent = db.limit_videos(8)
    most_viewed = db.limit_videos(8, u'views')
    return render_template('index.html', videos=videos, recent=recent, most_viewed=most_viewed, log=log_msg)

@app.route('/b/<video>', methods=['GET', 'POST'])
def dinamic_route(video):
    video = db.get_video(video)
    another = db.limit_videos(24)
    db.update_video(video)
    return render_template('player.html', video=video, another=another)

@app.route('/upload_page', methods=['GET'])
def redirect_to_upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_videos():
    data = request.files
    id = id_gen()
    files = []
    error = []
    ext = []
    obj = {
        "id": id.generate_id(),
        "views": 0,
        "name": '',
        "thumbnail": '',
        "content": '',
        "date": str(datetime.today().strftime("%b %d %Y")),
        "creator": ""
    }
    obj['name'] = request.form.get('vid_name')
    for file in list(data):
        file_blob = data.get(file)
        file_name = file_blob.filename
        file_type = file_name.split('.')[-1]
        if file_type not in set(ext):
            ext.append(file_type)
            response = upload.download_file(file_blob, file_name)
            if response == None:
                if file_name not in set(files):
                    files.append(file_name)
            else:
                error.append(file_name)
        else:
            error.append(file_name)
    if error == []:
        if len(files) > 1:
            for file_name in files:
                file_url = stor.upload_file(obj.get('id'), file_name)
                file_type = file_type = file_name.split('.')[-1]
                if file_type in upload.ext.get('video'):
                    obj['content'] = file_url
                else:
                    obj['thumbnail'] = file_url
            db.new_video(obj.get('id'), obj)
            session['upload_log'] = 'O upload terminou com sucesso.\n' + str(len(files)) + 'arquivos sucedidos.'
        else:
            for file in os.listdir('./static/download'):
                os.remove('./static/download/'+file) 
            session['upload_log'] = 'O upload terminou com falha.\nLog: Arquivo ou tipo de arquivo em duplicidade.'
    else:
        for file in os.listdir('./static/download'):
            os.remove('./static/download/'+file)
        session['upload_log'] = 'O upload terminou com falha.\nLog: ' + str(len(error)) + ' arquivo(s) com erro.'
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = 'nasakuki20'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, use_reloader=True)