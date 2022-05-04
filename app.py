
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime, json
import requests
from flask import Flask, url_for, flash
from flask import render_template, request, redirect
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '2022'

cred = credentials.Certificate("firebase-key.json")
fire = firebase_admin.initialize_app(cred)
db = firestore.client()
tasks_ref = db.collection('tasks')
user_ref = db.collection('Users')
api_key = 'AIzaSyAlQvqgGh9OGIBqBmySEYVT3s5NO246Cio'
user_auth = False

def read_tasks(ref):
    docs = ref.get()
    all_tasks = []
    # return [task.to_dict() for task in docs]
    for doc in docs:
        task = doc.to_dict()
        task['id'] = doc.id
        all_tasks.append(task)

    return all_tasks

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

def login_fb(mail,password):
    credentials = {"email":mail,"password":password,"returnSecureToken":True}
    response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}'.format(api_key),data=credentials)
    if response.status_code == 200:
        content = response.content
        data = response.json()
    elif response.status_code == 400:
        print(response.status_code)
        data = 400
        

    return data

       
@app.route('/login', methods=['GET', 'POST'])
def login():
        global user_auth
        if request.method == 'GET':
          return render_template('login.html')
        else:
            mail = request.form['mail']
            password = request.form['password']
            user = login_fb(mail,password)
            try:
                if user == user['email']:
                      user_auth = True
                      return  redirect('/')
                else:
                     print("sesion fallida")
                     flash('Credenciales invalidas')
                     redirect('/')
            except:
                flash('Credenciales invalidas')
                redirect('/')
                return redirect('/')
                
   

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        if user_auth:
            try:
                tasks = read_tasks(tasks_ref)
                print(tasks)
                completed = []
                incompleted = []

                for task in tasks:
                    if task['check']==True:
                        completed.append(task)
                    else:
                        incompleted.append(task)
            except:
                tasks = []
                print("error")
            response = {
                'completed':completed,
                'incompleted':incompleted,
                'contador1':len(completed),
                'contador2':len(incompleted)
            }
            return render_template('index.html', response=response)
        else:
            return redirect(url_for('login'))
    else:
        name = request.form["name"]
        try:
            create_task(tasks_ref, name)
            return redirect('/')
        except:
            pass
    



    
    


@app.route('/update/<string:id>', methods=['GET'])
def update(id):
        # print(f"\nVas a actualizar {id}\n")
        # return redirect('/')
    try:
            update_task(tasks_ref, id)
            return redirect('/')
    except:
        return redirect('/')


@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    print(f"\nVas a borrar {id}\n")
    try:
        delete_task(tasks_ref, id)
        return redirect('/')
    except:
    
        return redirect('/')

@app.route('/logout', methods=['GET'])
def logout():
    user_auth = False
    return redirect('/')
 


if __name__ == '__main__':
    app.run(debug=True)
