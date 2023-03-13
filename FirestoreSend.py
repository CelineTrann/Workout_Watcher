import firebase_admin
from  firebase_admin import credentials
from firebase_admin import firestore
#from google.cloud import firestore

# initializations 

cred = credentials.Certificate("/home/pi/Desktop/qu-evergreen-firebase-adminsdk-pcu2s-73526791b5.json")
#firebase_admin.initialize_app(cred)
db = firestore.client()


#adding first data
doc_ref = db.collection('employee').document('empdoc')

doc_ref.set({

    'name':'Try',
    'lname':'??',
    'age':25


})