import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from os import path

class Task:
    def __init__(self):
        self.args = self.parse_args()
        self.logger = self.init_logger()

    def init_logger(self):
        ROOT = path.dirname(path.dirname(path.dirname(path.realpath(__file__))))
        log_path = path.join(ROOT, "executor.log")

        logger = logging.getLogger('task')
        logger.setLevel(logging.DEBUG)
        fh = RotatingFileHandler(log_path, mode='a', maxBytes=5 * 1024 * 1024,
                                 backupCount=2, encoding=None, delay=0)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - action:{} - task_id:{} - %(levelname)s - %(message)s'.format(
                self.args['action_name'], self.args['task_id']))
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger

    def parse_args(self):
        dict_args = json.loads(sys.argv[1].replace("'", "\""))
        return dict_args

    def run_logic(self):
        self.logger.info("im sending notification at url: {}".format(self.args['webHookToTrigger']))


Task().run_logic()
