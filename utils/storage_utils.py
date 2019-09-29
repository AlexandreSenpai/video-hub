from google.cloud import storage
import os
from datetime import datetime
from queue import Queue
from threading import Thread
import requests
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
    
    def json_generator(self, file_name, creator=None):
        obj = {
            "views": 0,
            "name": file_name,
            "date": str(datetime.today().strftime("%b %d %Y")),
            "creator": ""
        }
        with open('./static/download/blob_data.json', 'w', encoding='utf8') as data:
            data.write(json.dumps(obj))

    def upload_file(self, folder, file_name):
        self.set_cred()
        bucket_file_name = self.blob.blob(folder+'/'+file_name)
        bucket_file_name.upload_from_filename('./static/download/{}'.format(file_name))
        if file_name.split('.')[-1] in ['mp4', 'ogg', 'wmv']:
            self.json_generator(file_name)
            bucket_file_name = self.blob.blob(folder+'/blob_data.json')
            bucket_file_name.upload_from_filename('./static/download/blob_data.json')
            os.remove('./static/download/blob_data.json')
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
                    blob_url[parent[0]]['name'] = parent[1]
            elif parent[1].split('.')[-1] == 'json':
                data = requests.get(blob.public_url).json()
                blob_url[parent[0]]['name'] = data.get('name')
                blob_url[parent[0]]['creator'] = data.get('creator')
                blob_url[parent[0]]['date'] = data.get('date')
                blob_url[parent[0]]['views'] = data.get('views')
            else:
                blob_url[parent[0]]['thumbnail'] = blob.public_url
        return blob_url

    def list_recent_blobs(self, maximo):
        blob_url = {}
        index = 1
        for blob in self.blob.list_blobs():
            if index <= maximo:
                parent = blob.name.split('/')
                if parent[0] not in blob_url.keys():
                    blob_url[parent[0]] = {}
                if parent[1].split('.')[-1] in ['mp4', 'wmv']:
                        blob_url[parent[0]]['content'] = blob.public_url
                        blob_url[parent[0]]['name'] = parent[1]
                elif parent[1].split('.')[-1] == 'json':
                    data = requests.get(blob.public_url).json()
                    blob_url[parent[0]]['name'] = data.get('name')
                    blob_url[parent[0]]['creator'] = data.get('creator')
                    blob_url[parent[0]]['date'] = data.get('date')
                    blob_url[parent[0]]['views'] = data.get('views')
                else:
                    blob_url[parent[0]]['thumbnail'] = blob.public_url
                index += 1
            else:
                break
        return blob_url

if __name__ == '__main__':
    st = Storage()
    print(json.dumps(st.list_recent_blobs(), indent=4))