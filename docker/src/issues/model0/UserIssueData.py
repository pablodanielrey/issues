
from wamp_utils import JSONSerializable

class UserIssueData(JSONSerializable):

    def __init__(self):
        self.name = ''
        self.lastname = ''
        self.dni = ''
        self.photo = ''
        self.id = ''
