from flask import Flask
from flask import render_template
import datetime
import getpass
import crontab
from flask import request, jsonify
from monitor import app
import psutil
import json


@app.route("/")
def hello():
    return render_template('base.html')


class ProcessList(list):
    def __init__(self):
        super(ProcessList, self).__init__()
        self.extend(psutil.get_process_list())

    def sort_column(self, c='name', descending=False):
        if c == 'name':
            self.sort(key=lambda x: x.name)

        elif c == 'time-created':
            self.sort(key=lambda x: x.create_time, reverse=True)

        elif c == 'pid':
            self.sort(key=lambda x: x.pid)

    def names(self):
        names = []
        for process in self:
            names.append(process.name)
        return names


@app.route("/processes/")
def processes():
    p = ProcessList()
    user = getpass.getuser()
    sort = request.args.get('sort')
    if sort:
        p.sort_column(c=sort)
    return render_template("processes.html", processes=p, user=user)


@app.route("/processes/<int:pid>/status", methods=['GET'])
def process_status(pid):
    p = psutil.Process(pid)
    s = {}
    s['threads'] = p.get_num_threads()
    s['exe'] = p.exe
    s['cpu'] = p.get_cpu_percent(interval=1.0)
    s['ram'] = p.get_memory_percent()
    s['files'] = p.get_open_files()
    s['cwd'] = p.getcwd()

    return json.dumps(s)


@app.route("/processes/<int:pid>/kill", methods=['GET'])
def kill_process(pid):
    p = None
    try:
        p = psutil.Process(pid)
        p.terminate()
    except Exception:
        pass
    #return redirect(url_for('processes'))
    if p:
        return jsonify(killed=True, pid=p.pid)
    else:
        return jsonify(killed=False, pid=0)