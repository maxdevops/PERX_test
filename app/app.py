from datetime import datetime
from time import sleep
from celery import Celery
from celery.utils.iso8601 import parse_iso8601
from flask import Flask, request, jsonify, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

import flask_excel

from service import process_book_dict

app=Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "user": generate_password_hash("password")
}

flask_excel.init_excel(app)

app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/1'
celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)
celery.conf.update(
   result_extended=True
)


@celery.task
def run(book_dict, **kwargs):
    sleep(5) # чтобы увидеть "state":"PENDING"
    return process_book_dict(book_dict)


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def upload_file():
    if request.method == 'POST':
        book_dict = request.get_book_dict(field_name='file')
        task = run.apply_async([book_dict], {'date_start': datetime.utcnow()})
        return redirect(url_for('taskstatus', task_id=task.id))
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Upload Excell file (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
   </form>
    '''


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = run.AsyncResult(task_id)
    return jsonify({
        'state': task.state,
        'date_done': task.date_done,
        'result': task.result,
        'date_start': parse_iso8601(task.kwargs.get('date_start')) if task.kwargs else None,
    })


if __name__ == "__main__":
    app.run()
