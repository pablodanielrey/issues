import pyqrcode
import logging
import os
import sys
import uuid
from redmine import Redmine

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    r = Redmine(os.environ['ISSUES_REDMINE_URL'], key = os.environ['ISSUES_REDMINE_KEY'], version='3.3', requests={'verify': False})
    pcs = r.project.get('pcs')
    issues = r.issue.filter(project_id=pcs.id, status_id='*')

    for i in issues:
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
            continue

        qr = pyqrcode.create('http://pedidos.econo.unlp.edu.ar:3000/issues/{}'.format(i.id))
        fname = '/tmp/qr-{}.svg'.format(i.id)
        qr.svg(fname, scale=5, background="white", module_color="#000000")

        i.uploads = [{'path':fname, 'name':'qr-{}.svg'.format(i.id)}]
        i.save()
