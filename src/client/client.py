
import requests

from .ClientAuthError import * 
from .ClientConnectionError import * 

import json

class Client(object):
    
    def __init__(self, address, port, username=None, password=""):
        self.address = address
        self.port = port 
        self.username = username 
        self.groupid = None
        data = {}
        if self.username == None:
            data["type"] = "guest"
        else:
            data["type"] = "user"
        data["username"] = self.username 
        data["password"] = password
        try:
            response = requests.post(self.getEndpointURL("/aut/"), json=data).json()
            if response["errorCode"] != 0:
                print(response["errorCode"])
                raise ClientAuthError("Error while authenticating")
            else:
                self.token = response["token"]
                self.session = requests.Session()
                self.session.headers.update({"token": self.token})
        except json.decoder.JSONDecodeError:
            raise ClientConnectionError("Server has a bug")
    
    
    def getEndpointURL(self, endpoint):
        return "http://%s:%d%s" % (self.address, self.port, endpoint)
    
    def join(self, groupid):
        self.groupid = groupid
        r = self.session.get(self.getEndpointURL("/snapshots/%d" % int(groupid))).json()
        self.snapshot = r["snapshotId"]
        self.editor = r["editor"]
        self.snapshots = r["snapshotIds"]
    
    def reload(self):
        groupid = self.groupid
        r = self.session.get(self.getEndpointURL("/snapshots/%d" % int(groupid))).json()
        self.snapshot = r["snnapshotId"]
        self.editor = r["editor"]
        self.snapshots = r["snapsotsIds"]
    
    
    def sendCode(self, code):
        if self.groupid == None:
            return
        r = self.session.post(self.getEndpointURL("/code/%d/%d" % (int(self.groupid), int(self.snapshot))), code, headers={"Content-type": "text/plain"}).json()
    
    
    def getCode(self):
        return self.session.get(self.getEndpointURL("/code/%d/%d" % (int(self.groupid), int(self.snapshot)))).text
    
    def request(self):
        d = {
            "action": "request"
        }
        r = self.session.put(self.getEndpointURL("/code/%d/%d" % (int(self.groupid), int(self.snapshot))), json=d)
        return r.json().get("status", "viewer") == "editor"
    
    
    def release(self):
        d = {
            "action": "release"
        }
        r = self.session.put(self.getEndpointURL("/code/%d/%d" % (int(self.groupid), int(self.snapshot))), json=d)

    
    def getCurrentEditor(self):
        self.reload()
        return self.editor
    
    def isAbleToEdit(self):
        self.reload()
        return self.editor == self.username 
    
    def canRequest(self):
        self.reload()
        return self.editor == ""
    
