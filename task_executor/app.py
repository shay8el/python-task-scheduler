import thread

from flask import Flask
from flask_cors import CORS

from executor import Executor

executor_app = Flask(__name__)
CORS(executor_app)


@executor_app.route('/')
def index():
    with open("executor.log") as f:
        data = f.readlines()
    content = "".join(line + "<br>" for line in data)
    return "<body onLoad='window.scrollTo(0,99999)'>"+content+"</body>"


if __name__ == '__main__':
    max_age_days = 1
    executor = Executor(max_age_days=max_age_days)
    thread.start_new_thread(executor.run, ())
    executor_app.run(host='0.0.0.0', port=5001)
