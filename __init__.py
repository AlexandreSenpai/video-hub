from flask import Flask, render_template, request, redirect
from utils.download_file import Upload
from utils.storage import Storage

app = Flask(__name__, template_folder='./pages/')
stor = Storage()
upload = Upload()

@app.route('/', methods=['GET'])
def main_page():
    lista = stor.list_blobs()
    return render_template('index.html', list=lista)

@app.route('/b/<video>', methods=['GET', 'POST'])
def dinamic_route(video):
    lista = stor.list_blobs()
    url = lista[video]['content']
    return upload.display_download(url, video)

@app.route('/upload', methods=['POST'])
def upload_videos():
    data = request.files
    path = data.get('content').filename
    blob_info = {'thumbnail_url': '', 'content_url': ''}
    for file in list(data):
        file_blob = data.get(file)
        file_name = file_blob.filename   
        upload.download_file(file_blob, file_name)
        url = stor.upload_file(path, file_name)
        if file == 'content':
            blob_info['content_url'] = url
        else:
            blob_info['thumbnail_url'] = url
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)