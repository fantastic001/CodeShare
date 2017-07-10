
import requests 

class Client(object):

    def __init__(self, address, port, username):
        self.address = address
        self.port = port 
        self.username = username 
        self.groupname = ""

    def authenticate(self, password):
        pass
    
    def getEndpointURL(self, endpoint):
        return "http://%s:%d%s" % (self.address, self.port, endpoint)

    def join(self, groupname):
        self.groupname = groupname
        r = requests.post(self.getEndpointURL("/groups/%s/register/" % groupname), json={"name": self.username})
        print(r.status_code)

    def sendCode(self, code):
        if self.groupname == "":
            return
        r = requests.post(self.getEndpointURL("/groups/%s/code/" % self.groupname), code, headers={"Content-type": "text/plain"})

    def getCode(self):
        return requests.get(self.getEndpointURL("/groups/%s/code/" % self.groupname)).text

    def request(self):
        requests.post(self.getEndpointURL("/groups/%s/request/" % self.groupname), json={"name": self.username})


    def release(self):
        requests.post(self.getEndpointURL("/groups/%s/release/" % self.groupname))

    def getCurrentEditor(self):
        return requests.get(self.getEndpointURL("/groups/%s/editor/" % self.groupname)).json().get("name", "")

    def isAbleToEdit(self):
        return self.getCurrentEditor() == self.username

    def canRequest(self):
        return self.getCurrentEditor() == ""
