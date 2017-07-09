# coding: UTF-8

from server import * 
import random

from flask import Flask, request


import json 

app = Flask(__name__)

manager = GroupManager()

@app.route("/groups/<group>/register/", methods=["POST"])
def register(group):
    print(request.content_type)
    grp = manager.get_group_by_name(group)
    grp.add_user(User(request.get_json().get("name", "user-%d" % int(random.random()*1000)), "0.0.0.0"))
    return "OK"





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
