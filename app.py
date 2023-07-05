from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

app = Flask('app')

tasks = [
    {"id": 1,
     "title": "GET",
     "description": "Pobranie wszystkich zadan",
     "done": False},
    {"id": 2,
     "title": "GET",
     "description": "Pobranie konkretnego zadania",
     "done": False},
    {"id": 3,
     "title": "POST",
     "description": "Stworzenie nowego zadania",
     "done": False},
    {"id": 4,
     "title": "PUT",
     "description": "Modyfikacja konkretnego zadania",
     "done": False},
    {"id": 5,
     "title": "DELETE",
     "description": "Usuniecie konkretnego zadania",
     "done": False},
    {"id": 6,
     "title": "next",
     "description": "Taki se",
     "done": False},
    {"id": 7,
     "title": "nextyyt",
     "description": "Taki se zrob",
     "done": False},
]


# # pobranie wszystkich zadan url
# @app.route('/todo/api/v1.0/tasks')
# def all_tasks_url():
#     return jsonify({'tasks': [make_public_task(task) for task in tasks]})


# pobranie wszystkich zadan id
@app.route('/todo/api/v1.0/tasks_id')
@auth.login_required
def all_tasks_id():
    return jsonify({'tasks': tasks})


# pobranie jednego zadania
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


# dodanie pojedynczego zadania
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


# edycja zadania
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


# skasowanie zadania
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.pop(task_id - 1)
    return jsonify({'delete': f"Zadanie {task_id} zostalo usuniete"})


# make response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# url zamiast id
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


# autentykacja
@auth.get_password
def get_password(username):
    if username == 'kurs':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# # get tasks() tylko 5 pobran
@app.route('/todo/api/v1.0/tasks/<all>')
def get_tasks(all):
    task = all
    if task is None and task == "":
        return jsonify({'tasks': list(reversed(tasks[-5:]))})
    elif task == "all":
        return jsonify({'tasks': tasks})


# get tasks() tylko 5 pobran na dwie funkcje
# @app.route('/todo/api/v1.0/tasks/<all>', methods=['GET'])
# def get_tasks(all):
#     task = all
#     if task == "all":
#         return jsonify({'tasks': tasks})
#
#
# @app.route('/todo/api/v1.0/tasks/')
# def get_tasks_default():
#     return jsonify({'tasks': list(reversed(tasks[-5:]))})


if __name__ == "__main__":
    app.run(debug=True)
