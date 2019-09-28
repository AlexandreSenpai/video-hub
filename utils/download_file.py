from datetime import datetime
from flask import abort

class Upload:
    def __init__(self):
        self.ext = {
            'video': ['mp4', 'ogg'],
            'photo': ['jpg', 'jpeg', 'png', 'svg']
        }
        self.patt = {
            'video': '<video width="100%" autoplay><source src="{}" type="video/{}"></video>',
            'photo': '<img src="{}"/>'
        }
    
    def download_file(self, file, filename):
        try:
            if filename == '':
                file.save('./static/download/' + str(datetime.now()))
            else:
                file.save('./static/download/' + filename)
        except:
            abort(500)

    def display_download(self, url, filename):
        file_type = filename.split('.')[-1].lower()
        if file_type in self.ext['video']:
            return self.patt['video'].format(url, file_type)
        elif file_type in self.ext['photo']:
            return self.patt['photo'].format(url)
        else:
            return 'file extension not allowed.'