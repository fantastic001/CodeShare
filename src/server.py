# coding: UTF-8
 
import random
import sys
import json 
import hashlib
import time

from flask import Flask, request

from server import *
from userdb import *

app = Flask(__name__)

groupManager = GroupManager()
tokenManager = TokenManager()

db = None

"""	
autentificate

user:
	POST - new user
	PUT - update user
	DELETE - delete user
	
group:
	POST - new group
	PUT - update group
	DELETE - delete group

snapshot:
	POST - new snapshot
	PUT - update snapshot (update code)
	DELETE - delete snapshot
"""


""" autentificate
POST args: {
	"type" : <"user"/"guest">
	"username" : <username>
	"password" : <password>
}
ret : {
	"errorCode" : <
		0 - ok / 
		1 - wrong session type / 
		2 - wrong username or password /
		3 - could not generate token /
		4 - max number of guests reached > 
	"token" : <token>
}
"""
@app.route("/aut/", methods=["POST"])
def aut(group):
	ret = { "errorCode" : 0, "token" : "" }
	type = request.get_json().get("type", "")
	if type == "user":
		username = request.get_json().get("username", "")
		password = request.get_json().get("password", "")
		if len(username) == 0 or len(password) == 0:
			ret["errorCode"] = 2
		elif db.confirmUserLogin(username, hashPassword(password)):
			ret["token"] = tokenManager.newUser(username)
			if ret["token"] == "": 
				ret["token"] = tokenManager.getToken(username)
				if ret["token"] == "":
					ret["errorCode"] = 3
		else:
			ret["errorCode"] = 1
	elif type == "guest":
		ret["token"] = tokenManager.newGuest()
		if ret["token"] == -1: 
			ret["errorCode"] = 4
		elif ret["token"] == ""
			ret["errorCode"] = 3
	else: ret["errorCode"] = 2
	return json.dumps(ret)

	
""" universal header
	"token" : <token>
"""

""" user
POST args : {
	"username" : <username>
	"password" : <password>
}
PUT args : {
	"password" : <password>"
}
DELETE args : {
}
ret : {
	"errorCode" : <
		0 - ok / 
		1 - token not sent /
		2 - invalid http method 
		3 - invalid username or password > 
}
"""
@app.route("/user/", methods=["POST", "PUT", "DELETE"])
def userAction(username):
	ret = { "errorCode" : 0 }
	if request.method == "POST":
		username = request.get_json().get("username", "")
		password = request.get_json().get("password", "")
		if len(username) == 0 or len(password) == 0: 
			ret["errorCode"] = 3
		else:
			db.registerUser(username, hashPassword(password))
	elif request.method == "PUT":
		if not "token" in request.header: ret["errorCode"] = 1
		password = request.get_json().get("password", "")
		if len(password) == 0: 
			ret["errorCode"] = 3
		else:
			user = db.getUser(tokenManager.getUser(requesr.header["token"]))
			user.setPassWord(hashPassword(password))
			db.updateUser(user)
	elif request.method == "DELETE":
		if not "token" in request.header: ret["errorCode"] = 1
		password = request.get_json().get("password", "")
		if len(password) == 0: 
			ret["errorCode"] = 3
		else:
			db.removeUser(tokenManager.getUser(requesr.header["token"]))
	else ret["errorCode"] = 2
	return


	
	
	
	
	
	
	
	
@app.route("/groups/<group>/register/", methods=["POST"])
def register(group):
    grp = groupManager.get_group_by_name(group)
    grp.addMember(User(request.get_json().get("name", "user-%d" % int(random.random()*1000)), "0.0.0.0"))
    return "OK"


@app.route("/groups/<group>/editor/")
def who_edits(group):
    editor = groupManager.get_group_by_name(group).whoEdits()
    if editor != None:
        return editor.to_json()
    else:
        return "{}"


@app.route("/groups/<group>/request/", methods=["POST"])
def request_insert(group):
    grp = groupManager.get_group_by_name(group)
    ok = grp.setEditorByName(request.get_json()["name"])
    s = "rejected"
    if ok:
        s = "approved"
    return json.dumps({"status": s})

@app.route("/groups/<group>/release/", methods=["POST"])
def editor_release(group):
    name = request.get_json().get("name", "")
    groupManager.get_group_by_name(group).releaseEditor(name)
    return ""

@app.route("/groups/<group>/code/", methods=["GET","POST"])
def code_handling(group):
	if request.method == "GET":
		return groupManager.get_group_by_name(group).getCode()
	else:
		print(request.data)
		groupManager.get_group_by_name(group).setCode(request.data)
		return "OK"
		
def hashPassword(password):
	return hashlib.sha256(password.encode("utf-8")).hexdigest()

if __name__ == '__main__':
	try:
		db = UserDBJson("userdb/db.json")
		app.run(host=sys.argv[1], port=5000, debug=True)
	except FileNotFoundError as e:
		print ("DB file not found.")
		
		
