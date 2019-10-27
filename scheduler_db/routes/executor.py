from flask import request
from flask_restful import Resource

from DAL.sql_connector import DBConnector


class Executor(Resource):
    def get(self):
        data = request.form
        db_connector = DBConnector()
        return db_connector.get_pending_tasks_by_max_age_days(data['max_age_days'])

    def post(self):
        data = request.form
        db_connector = DBConnector()
        occurrence_id = db_connector.mark_task_as_done(data['task_id'])
        return occurrence_id
