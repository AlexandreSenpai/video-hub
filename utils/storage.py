from google.cloud import storage
import os
import json

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
    
    def list_blobs(self):
        blob_url = {}
        for blob in self.blob.list_blobs():
            parent = blob.name.split('/')
            if parent[0] not in blob_url.keys():
                blob_url[parent[0]] = {}
            if parent[1].split('.')[-1] in ['mp4', 'wmv']:
                    blob_url[parent[0]]['content'] = blob.public_url
                    blob_url[parent[0]]['id'] = blob.id.split('/')[-1]
                    blob_url[parent[0]]['name'] = parent[1]
            else:
                blob_url[parent[0]]['thumbnail'] = blob.public_url
        return blob_url

if __name__ == '__main__':
    st = Storage()
    print(json.dumps(st.list_blobs(), indent=4))