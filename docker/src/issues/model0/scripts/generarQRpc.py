import pyqrcode
import logging
import os
import sys
import uuid
from redmine import Redmine

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    url = sys.argv[1]
    issueId = url.split('/')[-1]
    logging.info('url : {}'.format(url))
    logging.info('issue : {}'.format(issueId))

    r = Redmine(os.environ['ISSUES_REDMINE_URL'], key = os.environ['ISSUES_REDMINE_KEY'], version='3.3', requests={'verify': False})
    i = r.issue.get(issueId)
    if not i:
        sys.exit(1)

    """
        TODO!!!
        ver si esto debe dejarse como parámetro en el environment
        o sea el custom field qr
    """
    qrc = {'id':6,'value':'1'}
    cfs = [cf for cf in i.custom_fields if cf.id == 6]
    if len(cfs) <= 0 or cfs[0].value == '0':
        i.custom_fields = [qrc]
    else:
        logging.info('Ya tiene generado un código qr')
        sys.exit(1)


    qr = pyqrcode.create(url)
    fname = '/tmp/qr-{}.svg'.format(issueId)
    qr.svg(fname, scale=5, background="white", module_color="#000000")



    i.uploads = [{'path':fname, 'name':'qr-{}.svg'.format(issueId)}]
    i.save()
