
class ClientAuthError(Exception):

    def __init__(self, msg):
        self.msg = msg 

    def getMessage(self):
        return self.msg
