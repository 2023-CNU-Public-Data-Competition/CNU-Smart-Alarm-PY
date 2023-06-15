from flask import Flask
import task
app = Flask(__name__)

@app.route('/task')
def task():
    task.task()
    return 'FINISH TASK'

if __name__ == '__main__':
    app.run(debug=True)