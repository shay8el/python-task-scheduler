from flask_restful import Resource

from DAL.sql_connector import DBConnector


class Actions(Resource):
    def get(self):
        db_connector = DBConnector()
        return db_connector.get_all_actions()

    def post(self):
        return "crate action"

class Action(Resource):
    def get(self, action_id):
        return "get action"

    def delete(self, action_id):
        return "delete action"

    def put(self, task_id):
        return "update action"
