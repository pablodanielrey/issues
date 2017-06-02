import logging
from autobahn.wamp.types import CallOptions, RegisterOptions
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner

def getWampUser(con, details):
    return {
        'id': 'asdsadsa'
    }

class WampComponent(ApplicationSession):

    def getLogger(self):
        return logging.getLogger('{}.{}'.format(self.__module__, self.__class__.__name__))

    def getRegisterOptions(self):
        return RegisterOptions(details_arg='details')

    async def onJoin(self, details):
        results = yield self.register(self, options=self.getRegisterOptions())
        results = yield self.subscribe(self)
