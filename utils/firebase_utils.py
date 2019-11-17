import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import firestore
class Auth:
    def __init__(self):    
        self.cred = credentials.Certificate("./credentials/firebase-cred.json")

    def initialize_app(self):
        app = firebase_admin.initialize_app(self.cred)
    
class firebase(Auth):
    def __init__(self):
        super().__init__()
        self.app = self.initialize_app()
        self.db = firestore.client()
        self.auth = firebase_admin.auth
    
    def new_video(self, vid_id, obj):
        doc = self.db.collection(u"videos").document(vid_id)
        doc.set(obj)
    
    def get_video(self, vid_id):
        video = self.db.collection(u"videos").document(vid_id)
        obj = video.get().to_dict()
        return obj
    
    def get_all_videos(self):
        docs = self.db.collection(u"videos").stream()
        for document in docs:
            print(document.to_dict())
    
    def limit_videos(self, index, custom_query=None):
        cities_ref = self.db.collection(u'videos')
        custom_qry = u'date' if custom_query == None else custom_query 
        ref = cities_ref.order_by(custom_qry, direction=firestore.Query.DESCENDING).limit(index)
        new_ref = ref.stream()
        for doc in new_ref:
            yield doc.to_dict()
    
    def update_video(self, vid_id):
        last = self.get_video(vid_id.get('id'))
        to_update = {"views": int(last.get('views')) + 1}
        doc = self.db.collection(u'videos').document(vid_id.get('id')).update(to_update)

    def create_user(self, user_email, user_pass):
        user_name = self.auth.create_user(email=user_email, password=user_pass)
        
if __name__ == '__main__':
    app = firebase()
    app.create_user('alexandrebsramos@hotmail.com', 'nasakuki20')