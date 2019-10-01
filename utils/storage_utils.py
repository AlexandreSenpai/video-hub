from google.cloud import storage
import os
from datetime import datetime

class Auth:
    def __init__(self):
        self.credentials = './credential/storage-cred.json'
        self.bucket = 'video-26857.appspot.com'
    
    def set_cred(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials
        os.environ['BUCKET'] = self.bucket

class Storage(Auth):
    def __init__(self):
        super().__init__()
        self.client = storage.Client()
        self.blob = self.client.get_bucket(self.bucket)
    
    def upload_file(self, folder, file_name):
        self.set_cred()
        bucket_file_name = self.blob.blob(folder+'/'+file_name)
        bucket_file_name.upload_from_filename('./static/download/{}'.format(file_name))
        os.remove('./static/download/{}'.format(file_name))
        return bucket_file_name.public_url