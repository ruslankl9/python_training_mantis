from sys import maxsize


class Project(object):

    def __init__(self, id=None, name=None, status=None, active=None, view_state=None, description=None):
        self.id = id
        self.name = name
        self.status = status
        self.active = active
        self.view_state = view_state
        self.description = description

    def __repr__(self):
        return "%s:%s:%s" % (self.id, self.name, self.description)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    @classmethod
    def id_or_max(self, pr):
        if pr.id:
            return int(pr.id)
        else:
            return maxsize