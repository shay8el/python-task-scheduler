import datetime

from flask_restful import Resource
from flask import request

from DAL.sql_connector import DBConnector


class Occurrences(Resource):
    def get(self):
        db_connector = DBConnector()
        if request.args.get('generic'):
            resp = db_connector.get_all_generic_occurrences()
        else:
            resp = db_connector.get_all_occurrences()
        return resp

    def post(self):
        data = request.get_json()
        db_connector = DBConnector()
        occurrence_id = db_connector.insert_occurrence(data['title'], data['details'], data.get('occurrenceDueTime'))
        return occurrence_id


class Occurrence(Resource):
    def get(self, occurrence_id):
        db_connector = DBConnector()
        return db_connector.get_occurrence_by_id(occurrence_id)

    def delete(self, occurrence_id):
        return "delete occurrence"

    def put(self, occurrence_id):
        data = request.get_json()
        db_connector = DBConnector()
        given_date_format = "%m/%d/%Y, %I:%M:%S %p"
        db_date_format = "%Y-%m-%d %H:%M:%S"
        formatted_date = datetime.datetime.strptime(data['taskDueTime'], given_date_format).strftime(db_date_format)

        task_id = db_connector.insert_task(occurrence_id, data['actionId'], data['distinction'], formatted_date,
                                           data['taskArgs'])
        return task_id
