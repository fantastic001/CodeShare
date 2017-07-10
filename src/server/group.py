
class Group(object):
    
    def __init__(self, name):
        self.name = name 
        self.editing = None
        self.queue = []
        self.users = [] 
        self.code = ""

    def add_user(self, user):
        self.users.append(user)

    def who_edits(self):
        """
        Returns User object who is currently editing

        None if noone edits
        """
        return self.editing

    def get_user_by_name(self, name):
        for user in self.users:
            if user.get_name() == name:
                return user 
        return None

    def set_editor_by_name(self, name):
        user = self.get_user_by_name(name)
        if self.editing != None and self.editing.get_name() == name:
            return True
        if len(self.queue) == 0:
            if self.editing == None:
                self.editing = user
                return True
            else:
                self.queue.append(user)
        else:
            if self.editing == None:
                self.editing = self.queue[0]
                self.queue = self.queue[1:]
                return self.editing.get_name() == name
            else:
                for q in self.queue:
                    if q.get_name() == name:
                        return False
                self.queue.append(user)
                return False
        return False
    
    def release_editor(self):
        self.editing = None
        if len(self.queue) > 0:
            self.editing = self.queue[0]
            self.queue = self.queue[1:]

    def set_code(self, code):
        self.code = code 

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name 
