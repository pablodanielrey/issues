import os
import logging
from autobahn.asyncio.wamp import ApplicationRunner

from issues.api.wamp import Issues

import txaio
txaio.use_asyncio()
txaio.start_logging(level='debug')

if __name__ == '__main__':

    logging.info('Ejecuando loop')

    runner = ApplicationRunner(
        url=os.environ['CROSSBAR_URL'],
        realm=os.environ['CROSSBAR_REALM']
    )

    runner.run(Issues)

    """
    		  this.getMyIssues = getMyIssues;
    		  this.getOfficesIssues = getOfficesIssues;
    		  this.getAssignedIssues = getAssignedIssues;
    		  this.findById = findById;
    			this.findByIds = findByIds;
    			this.findAll = findAll;
    		  this.create = create;
    		  this.createComment = createComment;
    		  this.changeStatus = changeStatus;
    			this.changePriority = changePriority;
    			this.getOffices = getOffices;
    			this.getAreas = getAreas;
    			this.getOfficeSubjects = getOfficeSubjects;
    			this.subscribe = subscribe;
    			this.searchUsers = searchUsers;
    			this.updateIssue = updateIssue;
    """
