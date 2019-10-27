import json
import os
import sqlite3

CONFIG = os.path.join('scheduler_db','DAL', 'config.json')


class DBConnector:
    def __init__(self, config_path=CONFIG):
        self.config = self.load_config_file(config_path)
        self.db_path = os.path.join(self.config['base_dir'], self.config['DB_name'])
        self.init_db_connection()

    @staticmethod
    def load_config_file(config_path):
        with open(config_path) as json_file:
            data = json.load(json_file)
            return data

    def init_db_connection(self):
        if not os.path.isfile(self.db_path):
            self.create_tables()
            self.insert_mock_data()
        self.connection = self.__setup_connection()

    def __setup_connection(self):
        return sqlite3.connect(self.db_path)

    def create_tables(self):
        path = os.path.join(self.config['base_dir'], self.config['schema_path'])
        qry = open(path, 'r').read()
        sqlite3.complete_statement(qry)
        conn = self.__setup_connection()
        cursor = conn.cursor()
        try:
            cursor.executescript(qry)
        except Exception as e:
            print e

    def insert_mock_data(self):
        path = os.path.join(self.config['base_dir'], self.config['mock_data_path'])
        qry = open(path, 'r').read()
        sqlite3.complete_statement(qry)
        conn = self.__setup_connection()
        cursor = conn.cursor()
        try:
            cursor.executescript(qry)
        except Exception as e:
            print e

    def __execute_insert_query(self, qry):
        conn = self.connection
        cursor = conn.cursor()
        try:
            cursor.execute(qry)
            inserted_id = cursor.lastrowid
            conn.commit()
            return inserted_id
        except Exception as e:
            raise e

    @staticmethod
    def parse_to_dict(keys, rows):
        return [{key: row[i] for i, key in enumerate(keys)} for row in rows]

    def __execute_select_query(self, qry, format_to_dict=False):
        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute(qry)
            keys = [key[0] for key in cursor.description]
            rows = cursor.fetchall()
        except Exception as e:
            print e
            raise e

        conn.commit()
        if format_to_dict:
            return self.parse_to_dict(keys, rows)
        return rows

    def __execute_update_query(self, qry):
        conn = self.connection
        cursor = conn.cursor()

        try:
            cursor.execute(qry)
        except Exception as e:
            print e
            raise e

        conn.commit()

    def __execute_bool_query(self, qry):
        rows = self.__execute_select_query(qry)
        return bool(rows[0][0])

    def get_all_occurrences(self):
        return self.get_all_by_table_name('occurrences')

    def mark_task_as_done(self, task_id):
        qry = """
                UPDATE tasks
                SET status='DONE'
                WHERE id={0}
                                """.format(task_id)
        self.__execute_update_query(qry)

    def get_all_generic_occurrences(self):
        qry = """
                        SELECT * from occurrences
                        WHERE due_time IS NULL
                        """.format()
        rows = self.__execute_select_query(qry, True)
        return rows

    def get_pending_tasks_by_max_age_days(self, max_age_days):
        qry = """
                SELECT tasks.*, actions.name as action_name, actions.location as action_location, actions.args as default_args,
                occurrences.title as occurrences_title, occurrences.details
                from ((tasks
                INNER JOIN occurrences ON tasks.occurrence_id=occurrences.id)
                INNER JOIN actions ON tasks.action_id=actions.id)
                WHERE tasks.status='PENDING' and DATETIME(tasks.due_time) > DATETIME('now') and DATETIME(tasks.due_time)<DATETIME('now','+{days} day')
                """.format(days=max_age_days)
        rows = self.__execute_select_query(qry, True)
        return rows

    def get_all_actions(self):
        return self.get_all_by_table_name('actions')

    def get_all_by_table_name(self, table_name):
        qry = """
        SELECT * from {}
        """.format(table_name)
        rows = self.__execute_select_query(qry, True)
        return rows

    def get_occurrence_by_id(self, id):
        qry = """
                SELECT * from occurrences
                WHERE id={0}
                """.format(id)
        rows = self.__execute_select_query(qry, True)
        return rows

    @staticmethod
    def format_value(input):
        asciiInput = str(input).encode('ascii', 'ignore').replace("'", "''")
        return asciiInput

    def insert_occurrence(self, title, details, due_time=None):
        if due_time:
            qry = "insert into occurrences(title, details,due_time) values('{0}', '{1}','{2}')".format(
                self.format_value(title),
                self.format_value(details),
                self.format_value(due_time))
        else:
            qry = "insert into occurrences(title, details) values('{0}', '{1}')".format(
                self.format_value(title),
                self.format_value(details))
        occurrence_id = self.__execute_insert_query(qry)
        return occurrence_id

    def insert_task(self, occurrence_id, action_id, distinction, due_time, taskArgs='{}'):
        qry = "insert into tasks(occurrence_id, action_id,distinction,due_time,task_args) values({0}, {1},'{2}','{3}','{4}')".format(
            occurrence_id, action_id,
            self.format_value(distinction),
            self.format_value(due_time),
            self.format_value(taskArgs))
        occurrence_id = self.__execute_insert_query(qry)
        return occurrence_id
