from flask import Flask, render_template, request, redirect
from utils.download_file import Upload
from utils.storage_utils import Storage
from utils.tk_generator import id_gen
import os

app = Flask(__name__, template_folder='./pages/')
stor = Storage()
upload = Upload()

@app.route('/', methods=['GET'])
def main_page():
    blob_list = stor.list_blobs()
    recent_list = stor.list_recent_blobs(24)
    return render_template('index.html', blob_list=blob_list, recent=recent_list)

@app.route('/b/<video>', methods=['GET', 'POST'])
def dinamic_route(video):
    lista = stor.list_recent_blobs(24)
    url = lista[video]['content']
    name = lista[video]['name']
    views = lista[video]['views']
    creator = lista[video].get('creator')
    date = lista[video]['date']
    return render_template('player.html', video=upload.display_download(url, name, views, creator, date), blob_info=lista)

@app.route('/upload_page', methods=['GET'])
def redirect_to_upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_videos():
    data = request.files
    id = id_gen()
    folder = id.generate_id()
    files = []
    error = []
    for file in list(data):
        file_blob = data.get(file)
        file_name = file_blob.filename  
        response = upload.download_file(file_blob, file_name)
        if response == None:
            files.append(file_name)
        else:
            error.append(file_name)
    
    print(error)
    print(files)
    if error == []:
        for file_name in files:
            stor.upload_file(folder, file_name)
    else:
        for file in os.listdir('./static/download'):
            os.remove('./static/download/'+file)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)