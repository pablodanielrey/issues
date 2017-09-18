import os
from redminelib import Redmine

class RedmineAPI:

    REDMINE_URL = os.environ['ISSUES_REDMINE_URL']
    KEY = os.environ['ISSUES_REDMINE_KEY']
    TRACKER_ERROR = 1
    TRACKER_COMMENT = 4
    STATUS_NEW = 1
    STATUS_WORKING = 2
    STATUS_FINISH = 3
    STATUS_CLOSE = 5
    CREATOR_FIELD = 1
    FROM_FIELD = 2

    @classmethod
    def _loadFile(cls, file):
        att = Attachment()
        att.id = file.id
        att.url = file.content_url
        att.size = file.filesize
        att.name = file.filename
        return att

    officeRedmineIdCache = {}
    officeIdCache = {}
    officeCache = {}

    @classmethod
    def _loadOffice(cls, con, redmine, officeId):
        if officeId is None:
            return None

        id = None
        if officeId not in cls.officeRedmineIdCache.keys():
            project = redmine.project.get(officeId)
            id = project.identifier
            cls.officeRedmineIdCache[officeId] = id
            cls.officeIdCache[id] = officeId
        else:
            id = cls.officeRedmineIdCache[officeId]

        return cls._findOffice(con, id)

    @classmethod
    def _findOffice(cls, con, id):
        if id is None:
            return None

        office = None
        if id not in cls.officeCache.keys():
            offices = Office.findByIds(con, [id])
            office = offices[0] if len(offices) > 0 else None
            cls.officeCache[id] = office
        else:
            office = cls.officeCache[id]

        return office
        """
        offices = Office.findByIds(con, [id])
        office = offices[0] if len(offices) > 0 else None
        return office
        """


    """
    metodos codificados por ema sin cache.
    @classmethod
    def _loadOffice(cls, con, redmine, officeId):
        if officeId is None:
            return None

        offId = cls.officeRedmineIdCache[officeId]

        project = redmine.project.get(officeId)
        id = project.identifier
        return cls._findOffice(con, id)

    @classmethod
    def _findOffice(cls, con, id):
        if id is None:
            return None

        offices = Office.findByIds(con, [id])
        return offices[0] if len(offices) > 0 else None
    """

    @classmethod
    def _getCreatorOfficeId(cls, r):
        for cf in r.custom_fields:
            if cf.id == cls.FROM_FIELD:
                return cf.value
        return None

    @classmethod
    def _fromResult(cls, con, r, redmine, related=False):
        attrs = dir(r)
        issue = Issue()
        issue.id = r.id
        issue.parentId = [r.parent.id if 'parent' in attrs else None][0]
        issue.projectId =  [r.project.id if 'project' in attrs else None][0]

        office = cls._loadOffice(con, redmine, issue.projectId)
        if office is not None and office.type is not None and office.type['value'] == 'area':
            issue.area = office
            issue.office = cls._findOffice(con, office.parent)
        else:
            issue.area = None
            issue.office = office

        issue.projectName = [r.project.name if 'project' in attrs else None][0]

        issue.userId = cls._loadUserByUIdRedmine(con, r.author.id, redmine)
        issue.subject = r.subject
        issue.description = r.description

        issue.priority = r.priority.id
        issue.statusId = r.status.id
        issue.assignedToId =[r.assigned_to.id if 'assigned_to' in attrs else None][0]

        issue.start = Utils._localizeUtc(r.created_on) if Utils._isNaive(r.created_on) else r.created_on
        issue.updated = Utils._localizeUtc(r.updated_on) if Utils._isNaive(r.updated_on) else r.updated_on

        for cf in r.custom_fields:
            if cf.id == cls.CREATOR_FIELD:
                issue.creatorId = cf.value
            elif cf.id == cls.FROM_FIELD:
                issue.fromOfficeId = cf.value
                issue.fromOffice = cls._findOffice(con, issue.fromOfficeId)

        """
        if related:
            childrens = [iss.id for iss in r.children if iss is not None]
            issue.children = cls.findByIds(con, childrens)
        """
        issue.files = [cls._loadFile(file) for file in r.attachments if file is not None]

        return issue


    @classmethod
    def findByIds(cls, con, issuesIds, childrens=False, attachments=False):
        """ retorna los issues del modelo nuestro identificados por los ids issuesIds """
        assert isinstance(issuesIds, list)

        redmine = cls._getRedmineInstance()
        if redmine is None:
            return None

        includes = []
        if childrens:
            includes.append('childrens')
        if attachments:
            includes.append('attachments')

        issues = []
        for issueId in issuesIds:
            try:
                if len(includes) > 0:
                    issues.append(redmine.issue.get(issueId, include=','.join(includes)))
                else:
                    issues.append(redmine.issue.get(issueId))
            except Exception as e:
                logging.exception(e)
                logging.error('------------------------------------')
                logging.error('error obteniendo issue {}'.format(issueId))
                logging.error('------------------------------------')
        return [cls._fromResult(con, issue, redmine, True) for issue in issues]


    @classmethod
    def _findUserId(cls, con, redmine, userId):
        """ retorna el id del usuario de nuestra base a id de usuario de redmine """
        ups = UserPassword.findByUserId(con, userId)
        if len(ups) <= 0:
            return None
        up = ups[0]

        user = cls._getUserRedmine(up, userId, con)
        return user.id

    @classmethod
    def _getRedmineInstance(cls, con = None, userId = None, isImpersonate = False):
        if isImpersonate is None or not isImpersonate:
            return Redmine(cls.REDMINE_URL, key = cls.KEY, version='3.3', requests={'verify': False})
        else:
            ups = UserPassword.findByUserId(con, userId)
            if len(ups) <= 0:
                return None
            up = ups[0]
            userRedmine = cls._getUserRedmine(up, userId, con).login
            return Redmine(cls.REDMINE_URL, key = cls.KEY, impersonate = userRedmine, version='3.3', requests={'verify': False})

    @classmethod
    def _getUserRedmine(cls, up, uid, con):
        redmine = cls._getRedmineInstance(cls, con)
        user = up.username
        usersRedmine = redmine.user.filter(name=user)
        if len(usersRedmine) <= 0:
            usersRedmine = [cls._createUserRedmine(uid, up, con, redmine)]
        return usersRedmine[0]

    @classmethod
    def _createUserRedmine(cls, uid, up, con, redmine):
        u = User.findById(con, [uid])[0]
        mails = Mail.findByUserId(con, uid)
        mailsEcono = [ mail for mail in mails if '@econo.unlp.edu.ar' in mail.email]
        mail = mailsEcono[0].email if len(mailsEcono) > 0 else (mails[0].email if len(mails) > 0 else None)

        user = redmine.user.new()
        user.login = u.dni
        user.password = up.password
        user.firstname = u.name
        user.lastname = u.lastname
        user.mail = mail
        user.save()
        return user

    @classmethod
    def _loadUserByUIdRedmine(cls, con, uid, redmine):
        userRedmine = redmine.user.get(uid)
        dni = userRedmine.login if userRedmine != None and 'login' in dir(userRedmine) else None
        (userId, version) = User.findByDni(con, [dni])[0]
        return userId

    @classmethod
    def findAllProjects(cls):
        redmine = cls._getRedmineInstance()
        if redmine is None:
            return []
        projects = redmine.project.all()
        return [p.identifier for p in projects]

    @classmethod
    def getOfficesIssues(cls, con, officeIds):
        userIds = Office.findOfficesUsers(con, officeIds)
        issues = []
        for userId in userIds:
            issues.extend(cls.getMyIssues(con, userId))
        # return [cls._fromResult(con, issue) for issue in issues if not cls._include(issues,issue)]
        return [issue for issue in issues if not cls._include(issues,issue)]

    @classmethod
    def getMyIssues(cls, con, userId, statuses, froms, tos):
        redmine = cls._getRedmineInstance()
        user = cls._findUserId(con, redmine, userId)
        issues = cls._getIssuesByUser(con, user, statuses, froms, tos, redmine)
        return [issue for issue in issues]
        #return [cls._fromResult(con, issue, redmine) for issue in issues if not cls._include(issues,issue)]

    @classmethod
    def _getIssuesByUser(cls, con, userId, statuses, froms, tos, redmine):
        if redmine is None:
            return []

        issues = []
        if statuses is not None and len(statuses) > 0:
            for s in statuses:
                issues.extend(redmine.issue.filter(author_id=userId, status_id=s))
        else:
            issues.extend(redmine.issue.filter(author_id=userId, status_id='*'))

        """ elimino las que tienen padre """
        rissues = [issue.id for issue in issues if 'parent' not in dir(issue)]
        #return [issue.id for issue in issues]
        return rissues

    @classmethod
    # @do_cprofile
    def getAssignedIssues(cls, con, userId, oIds, froms=None, statuses=None):
        """
            Retorna una lista de issues asignados a las oficinas : oIds
            froms = de quien proviene el Issue. si es [] entonces retorna todos los que NO TENGAN oficina de origen. Si es None no se tiene en cuenta.
            statuses = estados de los issues. si es None no se tiene en cuenta como filtro.
        """
        assert isinstance(oIds,list)
        if len(oIds) <= 0:
            return []

        if statuses is not None:
            assert isinstance(statuses,list)
            if len(statuses) <= 0:
                return []

        redmine = cls._getRedmineInstance(con)
        userRedmine = cls._findUserId(con, redmine, userId)
        issues = cls._getIssuesByProject(con, oIds, froms, statuses, userRedmine, redmine)
        return list(set([i.id for i in issues]))

    @classmethod
    def _getIssuesByProject(cls, con, pIds, cIds, statuses, user, redmine):
        if redmine is None:
            return []
        issues = []
        projects = [p for p in redmine.project.all() if p.identifier in pIds]
        for project in projects:
            # issues.extend(redmine.issue.filter(tracker_id=cls.TRACKER_ERROR, project_id=pidentifier, subproject_id='!*', status_id='open'))

                if cIds is None:
                    issues.extend(redmine.issue.filter(tracker_id=cls.TRACKER_ERROR, project_id=project.id, status_id='*'))

                elif len(cIds) <= 0:
                    """
                        no tienen oficina origen
                    """
                    auxIssues = redmine.issue.filter(tracker_id=cls.TRACKER_ERROR, project_id=project.id, status_id='*')
                    issues.extend([iss for iss in auxIssues if not cls._hasCustomField(iss, RedmineAPI.FROM_FIELD)])

                else:
                    """
                    No funciona como dice la documentación!!. asi que lo filtro despues de obtenerlos MALISIMOO!!!

                    for cId in cIds:
                        logging.info('Filtrando por from_field {}'.format(cId))
                        cFields = [cls._getCustomFieldToFilter(RedmineAPI.FROM_FIELD, cId)]
                        issues.extend(redmine.issue.filter(tracker_id=cls.TRACKER_ERROR, project_id=pId, custom_fields=cFields, status_id='open'))
                    """

                    auxIssues = redmine.issue.filter(tracker_id=cls.TRACKER_ERROR, project_id=pId, status_id='*')
                    filteredIssues = set()
                    for cId in cIds:
                        filteredIssues.update([iss for iss in auxIssues if cls._hasCustomFieldValue(iss, RedmineAPI.FROM_FIELD, cId)])
                    issues.extend(filteredIssues)

                    """ agrego los pedidos que no tienen oficinas. si no se presta a confusión """
                    issues.extend([iss for iss in auxIssues if not cls._hasCustomField(iss, RedmineAPI.FROM_FIELD)])

        if statuses is not None and len(statuses) > 0:
            issues = [i for i in issues if i.status.id in statuses]

        return issues

    @classmethod
    def _include(cls, issues, issue):
        ids = []
        aux = issue

        while 'parent' in dir(aux) and aux.parent:
            ids.append(aux.id)
            aux = aux.parent

        for iss in issues:
            if iss.id in ids:
                return True
        return False

    @classmethod
    def create(cls, con, iss):
        redmine = cls._getRedmineInstance(con, iss.userId, True)
        if redmine is None:
            return None

        issue = redmine.issue.new()

        issue.project_id = iss.projectId
        issue.subject = iss.subject
        issue.description = iss.description
        issue.status_id = iss.statusId
        issue.parent_issue_id = iss.parentId
        issue.start_date = iss.start
        issue.tracker_id = iss.tracker
        issue.priority_id = iss.priority
        cfields = cls.getCustomFields(iss)
        if len(cfields) > 0:
            issue.custom_fields = cfields
        issue.uploads = iss.files
        issue.save()

        return issue.id


    """
        ///////////////////////////// CUSTOM FIELDS //////////////////////////////
        ////// FROM = oficina de la que viene el pedido
        ////// CREATOR = quien cargo el pedido
        ///////////
    """

    @classmethod
    def _hasCustomField(cls, issue, customId):
        for cf in issue.custom_fields:
            if cf['id'] == customId:
                if cf['value'] is not None and cf['value'].strip() != '':
                    return True
        return False

    @classmethod
    def _hasCustomFieldValue(cls, issue, customId, value):
        for cf in issue.custom_fields:
            if cf['id'] == customId and cf['value'] == value:
                return True
        return False

    @classmethod
    def _getCustomFieldToFilter(cls, customId, value):
        return {'id':customId, 'value': value}

    @classmethod
    def getCustomFields(cls, issue):
        custom_fields = []
        if issue.creatorId != issue.userId and issue.creatorId is not None:
            custom_fields.append({'id': RedmineAPI.CREATOR_FIELD, 'value': issue.creatorId})
        if issue.fromOfficeId is not None:
            custom_fields.append({'id': RedmineAPI.FROM_FIELD, 'value': issue.fromOfficeId})
        return custom_fields

    """
        //////////////////////////////////////////////
    """

    @classmethod
    def changeStatus(cls, issue_id, project_id, status):
        redmine = cls._getRedmineInstance()
        if status is None or redmine is None:
            return None
        return redmine.issue.update(issue_id, status_id = status)

    @classmethod
    def changePriority(cls, issue_id, project_id, priority):
        redmine = cls._getRedmineInstance()
        if priority is None or redmine is None:
            return None
        return redmine.issue.update(issue_id, priority_id = priority)
