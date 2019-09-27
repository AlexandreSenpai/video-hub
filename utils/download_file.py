from datetime import datetime

ext = {
    'video': ['mp4', 'avi', 'wmv', 'mov', 'ogg', 'mpg', 'mpeg', 'webm', 'flv'],
    'photo': ['jpg', 'jpeg', 'png', 'svg']
}
patt = {
    'video': '<video width="100%" autoplay><source src="{}" type="video/{}"></video>',
    'photo': '<img src="{}"/>'
}

def download_file(file, filename):
    try:
        if filename == '':
            saved = file.save('./static/download/' + str(datetime.now()))
        else:
            saved = file.save('./static/download/' + filename)
    except Exception as e:
        return 500

def display_download(filename):
    file_type = filename.split('.')[-1].lower()
    if file_type in ext['video']:
        return patt['video'].format(filename, file_type)
    elif file_type in ext['photo']:
        return patt['photo'].format(filename)
    else:
        return 'file extension not allowed.'