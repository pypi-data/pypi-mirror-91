from .scheme import call, get_scheme,HashcodeNotFound
from gevent.pywsgi import WSGIServer
from flask_cors import *
from flask import Flask, request, send_from_directory,abort, redirect
import json
import os
import webbrowser
import logging

# Meta info ,such as title,author,authentication,etc
META_INFO: {str: str} = {}

dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask("MIAO", static_url_path="", static_folder=os.path.join(dir_path, 'static'))
CORS(app, supports_credentials=True)


@app.route('/scheme')
def scheme():
    return json.dumps(get_scheme(), default=lambda info: info.get_dict())


@app.route('/call/<int:method_hash>', methods=['POST'])
def call_func(method_hash: int):
    body = request.get_data(as_text=True)
    parameters = json.loads(body)
    try:
        return_val = call(method_hash, *parameters)
        return json.dumps(return_val)
    except(HashcodeNotFound) :
        abort(412)


@app.route('/meta-info')
def meta_info():
    return META_INFO


@app.route('/')
def index():
    return redirect("/index.html", code=302)


# start MIAO server and block current python file
def start(title="MIAO", port: int = 2333, host: str = "0.0.0.0"):
    # TODO:add a logger
    print("MIAO's server is starting...")
    META_INFO['title'] = title
    http_server = WSGIServer((host, port), app, log=None)
    # http_server = WSGIServer((host, port), app)
    print_startup_done_message(host, port)
    http_server.start()
    webbrowser.open(get_hostname(host,port))
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("The MIAO's server is stopping")


def get_hostname(host,port):
    url = "http://"
    if host == "0.0.0.0":
        url += "localhost"
    else:
        url += host
    url+= ":" + str(port) + "/"
    return url
def print_startup_done_message(host, port):
    print("The MIAO's server started,\n" +
          "please enter this URL in your browser to access this application:\n"
          + get_hostname(host,port) )
