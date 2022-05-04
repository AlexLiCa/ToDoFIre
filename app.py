import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime, json
import requests

cred = credentials.Certificate("firebase-key.json")
fire = firebase_admin.initialize_app(cred)

db = firestore.client() #comunicacion con la base de datos 
api_key = 'AIzaSyAlQvqgGh9OGIBqBmySEYVT3s5NO246Cio'

#referencia a la coleccion de fb 
users_ref = db.collection('Users') #referencia a la colleccion de firebase

docs = users_ref.stream() #este objeto es una especie de lista  se puede mantener un tunel con mi aplicacion 
#docs = users_ref.get()  este objeto es una especie de lista  hace un snapshot en el momento y se tiene que refrescar para actualizar 


#esta funcion regresa una referencia a un usuario solo con el id 
def get_ref_user(id): 
    user_ref = users_ref.document(id)
    user = user_ref.get()
    if user.exists:
        docs_user_ref = user_ref.collection('tasks')
    else:
        docs_user_ref = False
    
    return docs_user_ref
    

def read_tasks(ref):
    docs = ref.get()
    #print(docs)
    for task in docs:
        print(f"ID{task.id} => DATA:{task.to_dict()}")
   

def read_task(ref, id):
    task = ref.document(id).get() #leer una solo un documento de firebase 
    #print(type(task))
    print(task.to_dict())

def create_task(ref, name):
    task = {
    'name': name,
    'check': False,
    'date':datetime.datetime.now()
}
    ref.document().set(task)

def update_task(ref,id):
    ref.document(id).update({'check': True})

def delete_task(ref,id):
    ref.document(id).delete()

def get_completed(ref):
    completed = ref.where('check','==', True).get()
    for task in completed:
        print(f"ID{task.id} => DATA:{task.to_dict()}")

def login(mail,password):
    credentials = {"email":mail,"password":password,"returnSecureToken":True}
    response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}'.format(api_key),data=credentials)
    if response.status_code == 200:
        content = response.content
        # llaves = response.json()['localId']
        llaves = response.json()['localId']

        print(type(llaves))  
        print(llaves)

        return llaves

      
   

    

    elif response.status_code == 400:
        pass


# create_task(new_task)
# update_task('3r8zqTLD2o2AJWLNMOFs')
# delete_task('3r8zqTLD2o2AJWLNMOFs')
 
email = 'alejandro@correo.com'
contraseña = 'Elchile'

login(email, contraseña)

ref_user = get_ref_user('GEmH20rxrihfDlxEMcBm')
#create_task(ref_user, 'No sirve')
#read_tasks(ref_user)