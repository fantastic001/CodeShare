
import json

class User(object):

    def __init__(self, name, ip):
        self.name = name 
        self.ip = ip 

    def get_name(self):
        return self.name 

    def get_ip(self):
        return self.ip 

    def to_json(self):
        d = {"name": self.name, "ip": self.ip}
        return json.dumps(d)
