


    def _getOfficesIssues(self, details):
        con = self.conn.get()
        self.conn.readOnly(con)
        try:
            userId = self.getUserId(con, details)
            oIds = Office.getOfficesByUser(con, userId, False)
            return Issue.getOfficesIssues(con, oIds)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.get_offices_issues')
    @inlineCallbacks
    def getOfficesIssues(self, details):
        r = yield threads.deferToThread(self._getOfficesIssues, details)
        returnValue(r)

    def _getAssignedIssues(self, statuses, froms, tos, details):
        """
            Retorna los issues asignados a las oficinas a las que pertenece la persona.
        """
        con = self.conn.get()
        self.conn.readOnly(con)
        try:
            if statuses is None:
                return []
            assert isinstance(statuses,list)
            if len(statuses) <= 0:
                return []

            userId = self.getUserId(con, details)
            oIds = Office.findByUser(con, userId, types=None, tree=True)
            toIds = [oid for oid in oIds if oid in tos]
            return Issue.getAssignedIssues(con, userId, toIds, froms, statuses)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.get_assigned_issues')
    @inlineCallbacks
    def getAssignedIssues(self, statuses, froms, tos, details):
        r = yield threads.deferToThread(self._getAssignedIssues, statuses, froms, tos, details)
        returnValue(r)

    def _findById(self, issueid, details):
        con = self.conn.get()
        self.conn.readOnly(con)
        try:
            issues = Issue.findByIds(con, [issueid])
            if issues is None or len(issues) <= 0:
                return None
            return issues[0]
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.find_by_id')
    @inlineCallbacks
    def findById(self, issueid, details):
        r = yield threads.deferToThread(self._findById, issueid, details)
        returnValue(r)

    def _findByIds(self, issuesIds, details):
        con = self.conn.get()
        self.conn.readOnly(con)
        try:
            logging.info(issuesIds)
            if len(issuesIds) <= 0:
                return []
            return Issue.findByIds(con, issuesIds)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.find_by_ids')
    @inlineCallbacks
    def findByIds(self, issuesIds, details):
        r = yield threads.deferToThread(self._findByIds, issuesIds, details)
        returnValue(r)

    def _create(self, subject, description, parentId, officeId, fromOfficeId, authorId, files, details):
        con = self.conn.get()
        try:
            print('create issue')
            userId = self.getUserId(con, details)
            authorId = userId if authorId is  None else authorId
            tracker = IssueModel.TRACKER_ERROR
            issueId = IssueModel.create(con, parentId, officeId, authorId, subject, description, fromOfficeId, userId, files, tracker)
            con.commit()
            return issueId

        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.create')
    @inlineCallbacks
    def create(self, subject, description, parentId, officeId, fromOfficeId, authorId, files, details):
        issueId = yield threads.deferToThread(self._create, subject, description, parentId, officeId, fromOfficeId, authorId, files, details)
        self.publish('issues.issue_created_event', issueId, authorId, fromOfficeId, officeId)
        returnValue(issueId)

    def _createComment(self, subject, description, parentId, projectId, files, details):
        con = self.conn.get()
        try:
            userId = self.getUserId(con, details)
            tracker = IssueModel.TRACKER_COMMENT
            issueId = IssueModel.create(con, parentId, projectId, userId, subject, description, '', '', files, tracker)
            con.commit()
            return issueId
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.create_comment')
    @inlineCallbacks
    def createComment(self, subject, description, parentId, projectId, files, details):
            issueId = yield threads.deferToThread(self._createComment, subject, description, parentId, projectId, files, details)
            self.publish('issues.comment_created_event', parentId, issueId)
            returnValue(issueId)

    @autobahn.wamp.register('issues.change_status')
    @inlineCallbacks
    def changeStatus(self, issue, status, details):
        iss = issue.changeStatus(status)
        yield self.publish('issues.updated_event', issue.id, status, issue.priority)
        return issue

    @autobahn.wamp.register('issues.change_priority')
    @inlineCallbacks
    def changePriority(self, issue, priority, details):
        iss = issue.changePriority(priority)
        yield self.publish('issues.updated_event', issue.id, issue.statusId, priority)
        return issue

    def _getOffices(self, details):
        con = self.conn.get()
        self.conn.readOnly(con)
        try:
            userId = self.getUserId(con, details)
            return IssueModel.getOffices(con, userId)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.get_offices')
    @inlineCallbacks
    def getOffices(self, details):
        offices = yield threads.deferToThread(self._getOffices, details)
        returnValue(offices)

    def _searchUsers(self, regex, details):
        con = self.conn.get()
        self.conn.readOnly(con)
        try:
            return IssueModel.searchUsers(con, regex)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.search_users')
    @inlineCallbacks
    def searchUsers(self, regex, details):
        users = yield threads.deferToThread(self._searchUsers, regex, details)
        returnValue(users)

    def _getOfficeSubjects(self, officeId, details):
        con = self.conn.get()
        self.conn.readOnly(con)
        try:
            return IssueModel.getSubjectTypes(con, officeId)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.get_office_subjects')
    @inlineCallbacks
    def getOfficeSubjects(self, officeId, details):
        sub = yield threads.deferToThread(self._getOfficeSubjects, officeId, details)
        returnValue(sub)

    def _getAreas(self, oId, details):
        con = self.conn.get()
        self.conn.readOnly(con)
        try:
            return IssueModel.getAreas(con, oId)
        finally:
            self.conn.put(con)

    @autobahn.wamp.register('issues.get_areas')
    @inlineCallbacks
    def getAreas(self, oId, details):
        areas = yield threads.deferToThread(self._getAreas, oId, details)
        returnValue(areas)
