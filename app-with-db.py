from logging import StringTemplateStyle
from flask import Flask
from flask_restful import Resource, Api, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'

db = SQLAlchemy(app)


class ToDoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    summary = db.Column(db.String(100))


db.create_all()


todos = {
    1: {'task': 'Task 1', 'summary': 'Summary 1'},
    2: {'task': 'Task 2', 'summary': 'Summary 2'},
    3: {'task': 'Task 3', 'summary': 'Summary 3'},
}

task_post_args = reqparse.RequestParser()

task_post_args.add_argument(
    "task", type=str, help="task is required", required=False)

task_post_args.add_argument("summary", type=str,
                            help="summary is required", required=False)

# update arguments
task_update_args = reqparse.RequestParser()
task_update_args.add_argument("task", type=str)
task_update_args.add_argument("summary", type=str)

resource_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'summary': fields.String
}


class ToDoList(Resource):
    def get(self):
        tasks = ToDoModel.query.all()
        todos = {}
        for task in tasks:
            todos[task.id] = {"task": task.task, "summary": task.summary}
        return todos


class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="could not find task with that id")
        return task

    @marshal_with(resource_fields)
    def post(self, todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()
        if task:
            abort(409, message="Taks ID already taken")
        args = task_post_args.parse_args()
        todo = ToDoModel(
            id=todo_id, task=args["task"], summary=args["summary"])
        db.session.add(todo)
        db.session.commit()
        return todo, 201

    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = task_update_args.parse_args()
        task = ToDoModel.query.filter_by(id=todo_id).first()

        if not task:
            abort(404, message="Taks does not exist, can not update")

        if args['task']:
            task.task = args['task']
        if args['summary']:
            task.summary = args['summary']

        db.session.commit()

        return task

    def delete(self, todo_id):
        task = ToDoModel.query.filter_by(id=todo_id).first()
        db.session.delete(task)
        return 'Todo Deleted', 204


api.add_resource(ToDo, '/todos/<int:todo_id>')
api.add_resource(ToDoList, '/', '/todos/')


if __name__ == "__main__":
    app.run(debug=True)
