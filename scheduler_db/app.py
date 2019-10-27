from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api

from routes.executor import Executor
from routes.occurrences import Occurrences, Occurrence
from routes.actions import Actions, Action

db_app = Flask(__name__)
api = Api(db_app)
CORS(db_app)

api.add_resource(Occurrences, '/occurrences')
api.add_resource(Occurrence, '/occurrences/<int:occurrence_id>')
api.add_resource(Actions, '/actions')
api.add_resource(Action, '/actions/<int:action_id>')
api.add_resource(Executor, '/executor')


@db_app.route('/')
def index():
    return render_template('creator.html')


if __name__ == '__main__':
    db_app.run()
