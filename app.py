from flask import Flask
from flask_restful import Resource, Api, abort, reqparse
app = Flask(__name__)
api = Api(app)

todos = {
    1: {'task': 'Task 1', 'summary': 'Summary 1'},
    2: {'task': 'Task 2', 'summary': 'Summary 2'},
    3: {'task': 'Task 3', 'summary': 'Summary 3'},
}

task_post_args = reqparse.RequestParser()

task_post_args.add_argument(
    "task", type=str, help="task is required", required=True)

task_post_args.add_argument("summary", type=str,
                            help="summary is required", required=True)


class ToDoList(Resource):
    def get(self):
        return todos


class ToDo(Resource):
    def get(self, todo_id):
        return todos[todo_id]

    def post(self, todo_id):
        print(f'todo is is {todo_id}')
        if todo_id in todos:
            abort(409, "Taks ID already taken")
        args = task_post_args.parse_args()
        todos[todo_id] = {"task": args["task"], "summary": args["summary"]}
        return todos[todo_id]


api.add_resource(ToDo, '/todos/<int:todo_id>')
api.add_resource(ToDoList, '/', '/todos/')


if __name__ == "__main__":
    app.run(debug=True)
