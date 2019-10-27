from datetime import datetime


class Task(object):
    def __init__(self, task_dict):
        self.due_time = datetime.strptime(task_dict['due_time'], "%Y-%m-%d %H:%M:%S")
        self.id = task_dict['id']
        self.task_dict = task_dict

    def __cmp__(self, other):
        return cmp(self.due_time, other.due_time)