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
    grp.set_editor_by_name(request.get_json()["name"])
    return ""

@app.route("/groups/<group>/release/", methods=["POST"])
def editor_release(group):
    manager.get_group_by_name(group).release_editor()
    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
