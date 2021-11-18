from flask import Flask, jsonify, render_template, redirect, flash, request
from flask_restful import Api, Resource, abort
from models import db, Todo
import logging
logging.basicConfig(filename='flask_server_logs.log', filemode='w', level=logging.DEBUG, format='%(asctime)s %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' )

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = '0zx5c34as65d4654&%^#$#$@'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/hello', methods=['GET'])
def hello():
    return "hello"


class TodoRUD(Resource):
    def get(self, *args, **kwargs):
        id = kwargs.get('todo_id')
        task = Todo.query.get(id)
        if not task:
            abort(404, message='Not Found')

        data = {
            'id': task.id,
            'name': task.name,
            'priority': task.priority,
            'description': task.description,
            'finished': task.finished
        }
        return data, 200

    def delete(self, *args, **kwargs):
        id = kwargs.get('todo_id')
        task = Todo.query.get(id)
        if not task:
            abort(404, message='Not Found')

        db.session.delete(task)
        db.session.commit()
        return {'message': 'Deleted Successfully'}, 200


    def patch(self, *args, **kwargs):
        id = kwargs.get('todo_id')
        task = Todo.query.get(id)
        if not task:
            abort(404, message='Not Found')
        if request.form.get('name'):
            task.name = request.form.get('name')
        if request.form.get('priority'):
            task.priority = request.form.get('priority')
        if request.form.get('description'):
            task.description = request.form.get('description')
        if request.form.get('finished'):
            task.finished = request.form.get('finished')
        db.session.commit()
        return {'message': 'Updated Successfully'}, 200



class TodoLC(Resource):
    def post(self):
        try:
            data = {
                'name': request.form.get('name'),
                'priority': request.form.get('priority'),
                'description': request.form.get('description'),
                'finished': False
            }

            task = Todo(**data)
            print(data)
            db.session.add(task)
            db.session.commit()
            return {'message': 'Task Created Successfully'}, 201
        except Exception as e:
            abort(500, message='Internal Server Error')


    def get(self):
        try:
            tasks = Todo.query.filter().all()
            list = []
            for task in tasks:
                data = {
                    'id': task.id,
                    'name': task.name,
                    'priority': task.priority,
                    'description': task.description,
                    'finished': task.finished
                }
                list.append(data)
            return list
        except Exception as e:
             abort(500, message="Internal Server Error {}".format(e))


api.add_resource(TodoLC, '/todo')
api.add_resource(TodoRUD, '/todo/<int:todo_id>')
db.init_app(app)


@app.before_first_request
def initiate_data_base_tables():
    db.create_all()

app.run(debug=True)

