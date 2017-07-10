# coding: UTF-8

from server import * 
import random

from flask import Flask, request


import json 

app = Flask(__name__)

manager = GroupManager()

@app.route("/groups/<group>/register/", methods=["POST"])
def register(group):
    grp = manager.get_group_by_name(group)
    grp.add_user(User(request.get_json().get("name", "user-%d" % int(random.random()*1000)), "0.0.0.0"))
    return "OK"



@app.route("/groups/<group>/editor/")
def who_edits(group):
    editor = manager.get_group_by_name(group).who_edits()
    if editor != None:
        return editor.to_json()
    else:
        return "{}"


@app.route("/groups/<group>/request/", methods=["POST"])
def request_insert(group):
    grp = manager.get_group_by_name(group)
    ok = grp.set_editor_by_name(request.get_json()["name"])
    s = "rejected"
    if ok:
        s = "approved"
    return json.dumps({"status": s})

@app.route("/groups/<group>/release/", methods=["POST"])
def editor_release(group):
    manager.get_group_by_name(group).release_editor()
    return ""

@app.route("/groups/<group>/code/", methods=["GET","POST"])
def code_handling(group):
    if request.method == "GET":
        return manager.get_group_by_name(group).get_code()
    else:
        print(request.data)
        manager.get_group_by_name(group).set_code(request.data)
        return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
