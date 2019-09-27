from flask import Flask, render_template, request, redirect
from utils.download_file import download_file, display_download
from utils.storage import Storage

app = Flask(__name__, template_folder='./pages/')

@app.route('/', methods=['GET'])
def main_page():
    return render_template('index.html', title='Usagi Video', text='Welcome to Google Cloud Platform')

@app.route('/upload', methods=['POST'])
def teste():
    stor = Storage()
    data = request.files['photo']
    file_name = data.filename   
    download_file(data, file_name)
    url = stor.upload_file(file_name)
    return display_download(url)

if __name__ == '__main__':
    app.run()