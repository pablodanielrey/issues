from autobahn.asyncio.wamp import ApplicationRunner
from wamp.issues import Issues

if __name__ == '__main__':

    runner = ApplicationRunner(
        os.environ['CROSSBAR_ROUTER']
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
