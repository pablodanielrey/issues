# -*- coding: utf-8 -*-
import asyncio
import os

import autobahn

from issues import api
from wamp_utils import WampComponent
from issues.model import Issues, UserIssueData, IssuesModel



class Issues(WampComponent):

    @autobahn.wamp.register('issues.get_my_issues')
    async def getMyIssues(self, statuses, froms, tos, details):
        """
            Obtiene los issues que realizó la oficina de la persona.
        """
        con = api.wamp.getConnection(readonly=True)
        try:
            userId = wamp.getWampUser(con, details)
            return Issues.getMyIssues(con, userId, statuses, froms, tos)
        finally:
            con.close()
