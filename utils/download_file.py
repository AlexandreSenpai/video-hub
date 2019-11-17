from datetime import datetime
class Upload:
    def __init__(self):
        self.ext = {
            'video': ['mp4', 'ogg'],
            'photo': ['jpg', 'jpeg', 'png', 'svg']
        }
        self.allowed = self.ext['video'] + self.ext['photo']

    def download_file(self, file, filename):
        file_type = filename.split('.')[-1]
        if filename != '':
            if file_type not in self.allowed:
                return filename
            else:
                file.save('./static/download/' + filename)
