
import requests 

from .ClientAuthException import * 

class Client(object):

    def __init__(self, address, port, username=None, password=""):
        self.address = address
        self.port = port 
        self.username = username 
        self.groupname = ""
        data = {}
        if self.username == None:
            data["type"] = "guest"
        else:
            data["type"] = "user"
        data["username"] = self.username 
        data["password"] = password
        response = requests.post(self.getEndpointURL("/aut/", json=data))
        if response["errorCode"] != 0:
            raise ClientAuthException("Error while authenticating")
        else:
            self.token = response["token"]
            self.session = requests.Session()
            self.session.headers.update({"token": self.token})

    
    def getEndpointURL(self, endpoint):
        return "http://%s:%d%s" % (self.address, self.port, endpoint)

    def join(self, groupname):
        self.groupname = groupname
        r = self.session.post(self.getEndpointURL("/groups/%s/register/" % groupname), json={"name": self.username})
        print(r.status_code)

    def sendCode(self, code):
        if self.groupname == "":
            return
        r = requests.post(self.getEndpointURL("/groups/%s/code/" % self.groupname), code, headers={"Content-type": "text/plain"})

    def getCode(self):
        return requests.get(self.getEndpointURL("/groups/%s/code/" % self.groupname)).text

    def request(self):
        r = requests.post(self.getEndpointURL("/groups/%s/request/" % self.groupname), json={"name": self.username})
        return r.json().get("status", "rejected") == "approved"


    def release(self):
        requests.post(self.getEndpointURL("/groups/%s/release/" % self.groupname), json={"name": self.username})

    def getCurrentEditor(self):
        return requests.get(self.getEndpointURL("/groups/%s/editor/" % self.groupname)).json().get("name", "")

    def isAbleToEdit(self):
        return self.getCurrentEditor() == self.username

    def canRequest(self):
        return self.getCurrentEditor() == ""
