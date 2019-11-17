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
    if 'upload_log' in session.keys():
        del session['upload_log']
    videos = db.limit_videos(48)
    recent = db.limit_videos(6)
    most_viewed = db.limit_videos(6, u'views')
    return render_template('index.html', videos=videos, recent=recent, most_viewed=most_viewed, log={"msg":log_msg})

@app.route('/b/<video>', methods=['GET'])
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
    def manage_data(files):
        for file_name in files:
            file_url = stor.upload_file(obj.get('id'), file_name)
            file_type = file_type = file_name.split('.')[-1]
            if file_type in upload.ext.get('video'):
                obj['content'] = file_url
            else:
                obj['thumbnail'] = file_url
        db.new_video(obj.get('id'), obj)
        session['upload_log'] = 'O upload terminou com sucesso.\n' + str(len(files)) + ' arquivo(s) sucedidos.'
        return redirect('/')
    def delete_files():
        for file in os.listdir('./static/download'):
            os.remove('./static/download/'+file)
    data = request.files
    id = id_gen()
    files = []
    error = []
    ext = []
    obj = {
        "id": id.generate_id(),
        "views": 0,
        "name": '',
        "thumbnail": 'https://firebasestorage.googleapis.com/v0/b/video-26857.appspot.com/o/resources%2Fno-thumb.jpg?alt=media&token=712f39b4-0220-4ee5-aa99-f4f0df798b00',
        "content": '',
        "date": datetime.today(),
        "creator": ""
    }
    obj['name'] = request.form.get('vid_name') if request.form.get('vid_name') != '' else 'sem título'
    for file in list(data):
        file_blob = data.get(file)
        file_name = file_blob.filename
        file_type = file_name.split('.')[-1]
        if file_type not in set(ext):
            ext.append(file_type)
            response = upload.download_file(file_blob, file_name)
            if response == None:
                if file_name not in set(files) and file_name != '':
                    files.append(file_name)
            else:
                error.append(file_name)
        else:
            error.append(file_name)
    has_vid = [True for f in ext if f in upload.ext['video']]
    if error == [] and True in has_vid:
            if len(files) < 2 and ext[0] in upload.ext['video']:
                manage_data(files)
                delete_files()
            else:
                manage_data(files)
                delete_files()
    else:
        delete_files()
        session['upload_log'] = 'O upload terminou com falha.\nLog: 1 ou mais arquivos com erro.'
        return redirect('/')
    return redirect('/')

@app.route('/join', methods=['GET'])
def join_us_page():
    return render_template('join.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    data = dict(request.form)
    user_email = data.get('email')
    user_pass = data.get('password')
    db.create_user(user_email, user_pass)
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = 'nasakuki20'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, use_reloader=True)