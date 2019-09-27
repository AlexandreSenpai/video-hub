from google.cloud import storage
import os

class Auth:
    def __init__(self):
        self.credentials = './credentials/storage-cred.json'
        self.bucket = os.environ['BUCKET']
    
    def set_cred(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.credentials

class Storage(Auth):
    def __init__(self):
        super().__init__()
        self.client = storage.Client()
        self.blob = self.client.get_bucket(self.bucket)
    
    def upload_file(self, file_name):
        self.set_cred()
        bucket_file_name = self.blob.blob(file_name)
        upload_file_name = bucket_file_name.upload_from_filename('./static/download/{}'.format(file_name))
        return bucket_file_name.public_url