# -*- coding: utf-8 -*-
import asyncio
import os

from wamp import WampComponent
from model.issues.issue import Issue


class Issues(WampComponent):

    @autobahn.wamp.register('issues.get_my_issues')
    async def getMyIssues(self, statuses, froms, tos, details):
        """
            Obtiene los issues que realizó la oficina de la persona.
        """
        con = wamp.getConnection(readonly=True)
        try:
            userId = getWampUser(con, details)
            return Issue.getMyIssues(con, userId, statuses, froms, tos)
        finally:
            con.close()
