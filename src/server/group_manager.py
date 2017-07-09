
from .group import * 

class GroupManager(object):
    
    def __init__(self):
        self.groups = [] 

    def get_group_by_name(self, name):
        """
        Returns group if given name 

        if there's no uch group, create new grup
        """
        for g in self.groups:
            if g.get_name() == name:
                return g 
        self.groups.append(Group(name))
        return self.get_group_by_name(name)
