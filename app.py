
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime, json
import requests
from flask import Flask
from flask import render_template, request, redirect
import requests


app = Flask(__name__)
cred = credentials.Certificate("firebase-key.json")
fire = firebase_admin.initialize_app(cred)
db = firestore.client()
tasks_ref = db.collection('tasks')
user_ref = db.collection('Users')


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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
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
    else:
        name = request.form["name"]
        print(name)
        try:
            create_task(tasks_ref, name)
            return redirect('/')
        except:
            pass

    return render_template('index.html', response=response)


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


if __name__ == '__main__':
    app.run(debug=True)
