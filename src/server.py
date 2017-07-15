# coding: UTF-8
 
import random, sys, json , hashlib, time, os

from flask import Flask, request

from server import *
from userdb import *

app = Flask(__name__)

groupManager = GroupManager()
tokenManager = TokenManager()

db = None

# activeGroups = { <groupid> : Group }
activeGroups = {}

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
		elif ret["token"] == "":
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
		1 - invalid http method /
		2 - token not sent /
		3 - invalid username or password > 
}
"""
@app.route("/user/", methods=["POST", "PUT", "DELETE"])
def userAction():
	ret = { "errorCode" : 0 }
	if request.method == "POST":
		username = request.get_json().get("username", "")
		password = request.get_json().get("password", "")
		if len(username) == 0 or len(password) == 0: 
			ret["errorCode"] = 3
		else:
			db.registerUser(username, hashPassword(password))
	elif request.method == "PUT":
		if not "token" in request.header: 
			ret["errorCode"] = 2
		else:
			password = request.get_json().get("password", "")
			if len(password) == 0: 
				ret["errorCode"] = 3
			else:
				user = db.getUser(tokenManager.getUser(request.header["token"]))
				user.setPassWord(hashPassword(password))
				db.updateUser(user)
	elif request.method == "DELETE":
		if not "token" in request.header: 
			ret["errorCode"] = 2
		else:
			password = request.get_json().get("password", "")
			if len(password) == 0: 
				ret["errorCode"] = 3
			else:
				db.removeUser(tokenManager.getUser(request.header["token"]))
	else: ret["errorCode"] = 1
	return ret

	
""" group
GET atgs : {}
POST args : {
	"groupname" : <groupname>
}
PUT args : {
}
DELETE args : {
	"groupid" : <groupid>
}
ret : {
	"groupid" : <groupid>
	"ownedGroups" : [<groupid>, ...]
	"errorCode" : <
		0 - ok /
		1 - invalid http method /
		2 - token not sent /
		3 - invalid group id /
		4 - only owner can delete the group /
		5 - unable to delete group >
}
"""
@app.route("/grups/", methods=["GET", "POST", "PUT", "DELETE"])
def grouAction():
	ret = { "errorCode" : 0 }
	if not "token" in request.header: 
		ret["errorCode"] = 2
	else:
		user = db.getUser(tokenManager.getUser(request.header["token"]))
		if request.method == "GET":
			ret["ownedGroups"] = []
			for group in db.getGroups():
				if group.getOwner().getName() == user.getName():
					ret["ownedGroups"].append(group.getId())
		elif request.method == "POST":
			groupname = request.get_json().get("groupname", "")
			group = db.createGroup(user, groupname)
			dir = "snapshots/" + str(group.getId())
			if not os.path.exists(dir): os.mkdir(dir)
			open("0.snap", "w")
			ret["groupid"] = group.getId()
		elif request.method == "PUT":
			group = getGroup(int(request.get_json().get("groupid", "")))
			if group == None:
				ret["errorCode"] = 3
			else:
				pass # group info update
		elif request.method == "DELETE":
			# delete files form disc
			groupid = request.get_json().get("groupid", "")
			group = getGroup(groupid)
			if group == None:
				ret["errorCode"] = 3
			else:
				if group.getOwner().getName() != user.getName():
					ret["errorCode"] = 4
				else:
					if db.removeGroup() == False:
						ret["errorCode"] = 5
					else:
						del activeGroups[groupid]
		else: ret["errorCode"] = 1
	return ret
	
	
""" snapshots
GET args : {}
POST args : {}
ret : {
	"snapshotIds" : [<snapshotId>, ...]
	"snapshotId" : <id of new ss>
	"editor" : <username>
	"errorCode" : <
		0 - ok /
		1 - invalid http method /
		2 - token not sent /
		3 - invalid groupid parameter >
}
"""
@app.route("/snapshots/<groupid>", methods=["GET", "POST"])
def snapshotAction(groupid):
	ret = { "errorCode" : 0 }
	if not "token" in request.header: 
		ret["errorCode"] = 2
	else:
		id = -1
		try: id = int(groupid)
		except: pass
		group = getGroup(id)
		if group == None:
			ret["errorCode"] = 3
		else:
			if request.method == "GET":
				ret[snapshotIds] = [ss.getId() for ss in group.getSnapshots()]
				if not snapshotid in activeGroups:
					activeGroups[snapshotId] = { "editor" : "", "snapshot" : len(group.getSnapshots) - 1 }
				ret[snapshotid] = activeGroups[group.getId()]["snapshot"]
				ret[editor] = activeGroups[group.getId()]["snapshot"]
			elif request.method == "POST":
				newId = group.getSnapshots()[-1].getId() + 1
				# copy current text file to new file
				group.addSnapshot(Snapshot(newId))
				ret["snapshotId"] = newId
			else:
				ret["errorCode"] = 1
	return ret
	
""" code
GET args : {}
POST args : <code>
PUT args : {
	"action" : <"request" / "release">
}
ret : {
	"status" : <"editor" / "viewer">
	"errorCode" : <
		0 - ok /
		1 - invalid http method /
		2 - token not sent /
		3 - invalid groupid parameter /
		4 - invalid snapshotid parameter >
"""
@app.route("/code/<groupid>/<snapshotid>", methods=["GET", "POST", "PUT"])
def codeAction(groupid, snapshotid):
	ret = { "errorCode" : 0 }
	if not "token" in request.header: 
		ret["errorCode"] = 2
	else:
		id = -1
		try: id = int(groupid)
		except: pass
		group = getGroup(id)
		if group == None:
			ret["errorCode"] = 3
		else:
			id = -1
			try: id = int(snapshotid)
			except: pass
			group = db.getGroup(id)
			if group == None:
				ret["errorCode"] = 4
			else:
				if request.method == "GET":
					pass
				elif request.method == "POST":
					pass
				elif request.method == "PUT":
					pass
				else:
					ret["errorCode"] = 1
	return ret
	
	
	
	
	
	
	
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
	
def getGroup(groupid):
	if groupid in activeGroups:	return activeGroups[groupid]
	else: return db.getGroup(groupid)

# args: host ip address
if __name__ == '__main__':
	try:
		db = UserDBJson("userdb/db.json")
		app.run(host=sys.argv[1], port=5000, debug=True)
	except FileNotFoundError as e:
		print ("DB file not found.")
		
		
