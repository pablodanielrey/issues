from wamp_utils import JSONSerializable
from issues.model.RedmineAPI import RedmineAPI


class Issues(JSONSerializable):

    def __init__(self):
        self.id = None
        self.parentId = None
        self.projectId = None
        self.office = None
        self.priority = 2
        self.area = None
        self.userId = None
        self.subject = ''
        self.description = None
        self.statusId = 1
        self.assignedToId = None
        self.files = []
        self.start = datetime.date.today()
        self.updated = None
        self.children = []
        self.files = []
        self.tracker = RedmineAPI.TRACKER_ERROR
        self.fromOfficeId = None
        self.creatorId = None

    @classmethod
    def findById(cls, con, id):
        return RedmineAPI.findByIds(con, [id])

    @classmethod
    def findByIds(cls, con, ids):
        return RedmineAPI.findByIds(con, ids)

    @classmethod
    def getOfficesIssues(cls, con, officeIds):
        return RedmineAPI.getOfficesIssues(con, officeIds)

    @classmethod
    def getMyIssues(cls, con, userId, statuses, froms, tos):
        return RedmineAPI.getMyIssues(con, userId, statuses, froms, tos)

    @classmethod
    def getAssignedIssues(cls, con, userId, oIds, statuses, froms):
        return RedmineAPI.getAssignedIssues(con, userId, oIds, statuses, froms)

    def changeStatus(self, status):
        return RedmineAPI.changeStatus(self.id, self.projectId, status)

    def changePriority(self, priority):
        return RedmineAPI.changePriority(self.id, self.projectId, priority)

    def create(self, con):
        return RedmineAPI.create(con, self)


class Attachment(JSONSerializable):

    def __init__(self):
        self.id = ''
        self.url = ''
        self.size = 0
        self.name = ''
