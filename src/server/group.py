
class Group(object):
    
    def __init__(self, name):
        self.name = name 
        self.editing = None
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

    def set_editor_by_name(self, name):
        for user in self.users:
            if user.get_name() == name:
                self.editing = user
                return 
    
    def release_editor(self):
        self.editing = None

    def set_code(self, code):
        self.code = code 

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name 
