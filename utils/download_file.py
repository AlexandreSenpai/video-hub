from datetime import datetime
from flask import abort, flash

class Upload:
    def __init__(self):
        self.ext = {
            'video': ['mp4', 'ogg'],
            'photo': ['jpg', 'jpeg', 'png', 'svg']
        }
        self.patt = {
            'photo': '<img src="{}"/>'
        }

        self.allowed = self.ext['video'] + self.ext['photo']

    
    def download_file(self, file, filename):
        file_type = filename.split('.')[-1]
        if file_type not in self.allowed:
            return filename
        else:
            file.save('./static/download/' + filename)

    def display_download(self, url, filename, views, creator, date):
        file_type = filename.split('.')[-1].lower()
        if file_type in self.ext['video']:
            obj = {'url': url, 'type': file_type, 'name': filename, 'views': views, 'creator': creator, 'date': date}
            return obj
        elif file_type in self.ext['photo']:
            return self.patt['photo'].format(url)
        else:
            return 'file extension not allowed.'