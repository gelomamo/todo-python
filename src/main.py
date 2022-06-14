"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

todos = [
    { "label": "My first task", "done": False }
]

@app.route('/todos', methods=['GET'])
def get_task():
    tarea = Task.query.all()
    all_task = list(map(lambda todos: todos.serialize(), tarea))
    return jsonify(all_task)

@app.route('/todos', methods=['POST'])
def crear():
    body = request.get_json()
    print(body)
    tarea = Task(text=body["label"], done=False)
    db.session.add(tarea)
    db.session.commit()
    return jsonify(tarea.serialize())

@app.route('/todos/<int:task_id>', methods=['PUT','GET','DELETE'])
def handle_task(task_id):
    if request.method == 'PUT':
        if task is None:
           raise APIException("Tarea no encontrada", 404) 
        body = request.get_json()
        if not ("done" is body):
            raise APIException("Parametro done no encontrado", 404) 
        task.done = body["done"]
        db.session.commit()
        return jsonify(task.serialize())

    elif request.method == 'GET':
        task = Task.query.get(task_id)
        if task is None:
           raise APIException("Tarea no encontrada", 404) 
        return jsonify(task.serialize())

    elif request.method == 'DELETE':
        task = Task.query.get(task_id)
        if task is None:
           raise APIException("Tarea no encontrada", 404)
        db.session.delete(task)
        db.session.commit()
        return jsonify(task.serialize())

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
