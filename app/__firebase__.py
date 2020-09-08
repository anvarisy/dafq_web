import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
# Use a service account

cred = credentials.Certificate('config.json')
firebase_admin.initialize_app(cred,{
     'storageBucket': 'pondok-f2805.appspot.com'
})

db = firestore.client()
bkt = storage.bucket()