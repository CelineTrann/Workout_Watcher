import firebase_admin
from  firebase_admin import credentials
from firebase_admin import firestore
#from google.cloud import firestore

# initializations 
cred = credentials.Certificate("workoutwatcher-654cd-firebase-adminsdk-xkutc-a7c0fc0bc5.json")
firebase_admin.initialize_app(cred)

#firebase_admin.initialize_app(cred)
db = firestore.client()


#adding first data
doc_ref = db.collection('employee').document('empdoc')

doc_ref.set({
    'name':'Try',
    'lname':'??'
})

doc_ref.update({
    'name':'Maisha',
    'lname':'Shahriar'
})