import json
import logging
import sys


class Task:
    def __init__(self):
        self.args = self.parse_args()
        self.logger = self.init_logger()

    def init_logger(self):
        logger = logging.getLogger('task')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('executor.log')
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
        self.logger.info("im sending email to {}".format(self.args['recipientAddress']))


Task().run_logic()
