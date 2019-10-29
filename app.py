import threading
from os import path
from flask import Flask, render_template
from flask_restful import Api

from executor.executor import Executor
from routes.occurrences import Occurrences, Occurrence
from routes.actions import Actions, Action

app = Flask(__name__)
api = Api(app)

api.add_resource(Occurrences, '/occurrences')
api.add_resource(Occurrence, '/occurrences/<int:occurrence_id>')
api.add_resource(Actions, '/actions')
api.add_resource(Action, '/actions/<int:action_id>')


@app.before_first_request
def activate_executor():
    max_age_days = 1
    executor = Executor(max_age_days=max_age_days)
    thread = threading.Thread(target=executor.run)
    thread.start()


@app.route('/')
def index():
    ROOT = path.dirname(path.realpath(__file__))
    log_path = path.join(ROOT, "executor.log")
    with open(log_path) as f:
        data = f.readlines()
    executor_data = "".join(line + " \r\n " for line in data)

    return render_template('creator.html', executor_data=executor_data)


if __name__ == '__main__':
    app.run()
