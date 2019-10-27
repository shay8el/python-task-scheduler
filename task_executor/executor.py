import Queue
import json
import subprocess
import sys
import time

import requests
import logging
from datetime import timedelta, datetime

from task import Task


class Executor:
    def __init__(self, max_age_days=1):
        self.logger = self.init_logger()
        self.MAX_AGE_DAYS = timedelta(days=max_age_days)
        self.queue = Queue.PriorityQueue()
        self.id_set = set()
        self.add_tasks_to_queue(self.fetch_tasks())

    def init_logger(self):
        logger = logging.getLogger('executor')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('executor.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def fetch_tasks(self):
        url = "http://127.0.0.1:5000/executor"
        data = {'max_age_days': self.MAX_AGE_DAYS.days}
        response = requests.get(url,data=data)
        response.raise_for_status()
        return response.json()

    def add_tasks_to_queue(self, tasks):
        for task_dict in tasks:
            t = Task(task_dict)
            if not self.is_far_fetched(t.due_time) and t.id not in self.id_set:
                self.id_set.add(t.id)
                self.queue.put(t)

    @staticmethod
    def is_task_time_apply(first_task_time):
        return first_task_time < datetime.now()

    def is_far_fetched(self, task_due_time):
        return task_due_time > datetime.now() + self.MAX_AGE_DAYS

    @staticmethod
    def merge_two_dicts(x, y):
        z = x.copy()
        z.update(y)
        return z

    def execute_task(self, task):
        self.logger.info("task_id: {}".format(task.id))
        action_location = task.task_dict['action_location']
        default_args = json.loads(task.task_dict['default_args'].replace("'", "\""))
        task_args = json.loads(task.task_dict['task_args'].replace("'", "\""))
        args_dict = self.merge_two_dicts(default_args, task_args)
        args_dict['action_name'] = task.task_dict['action_name']
        args_dict['task_id'] = task.id
        args = json.dumps(args_dict)
        subprocess.call([sys.executable, action_location, args])

    def mark_task_as_done(self, task_id):
        url = "http://127.0.0.1:5000/executor"
        data = {'task_id': task_id}
        response = requests.post(url, data=data)
        response.raise_for_status()
        self.logger.info("task_id {} marked as done".format(task_id))

    def run(self):
        SAMPLE_INTERVAL_SECONDS = 2
        while True:
            while not self.queue.empty():
                first_task_time = self.queue.queue[0].due_time
                if self.is_task_time_apply(first_task_time):
                    task = self.queue.get()
                    self.execute_task(task)
                    self.mark_task_as_done(task.id)
                else:
                    self.logger.debug(
                        "I have a {0} tasks waiting | next at: {1}".format(len(self.queue.queue), first_task_time))
                time.sleep(SAMPLE_INTERVAL_SECONDS)
                self.add_tasks_to_queue(self.fetch_tasks())
            self.logger.debug("I have no tasks")
            self.add_tasks_to_queue(self.fetch_tasks())
            time.sleep(SAMPLE_INTERVAL_SECONDS)
