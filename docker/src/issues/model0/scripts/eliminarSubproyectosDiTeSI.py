import psycopg2
import logging
import os
import sys
from redmine import Redmine
from redmine.exceptions import ResourceNotFoundError

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    r = Redmine(os.environ['ISSUES_REDMINE_URL'], key = os.environ['ISSUES_REDMINE_KEY'], version='3.3', requests={'verify': False})

    # id de la oficina de DiTeSI
    dId = '117ae745-acb3-48df-9005-343538f85403'
    pId = r.project.get(dId).id
    logging.info('Id del projecto DiTeSI en pedidos: {}'.format(pId))

    ppId = dId + '_'
    for p in r.project.all():
        if ppId in p.identifier:
            logging.info('Eliminando : {}'.format(p.name))
            r.project.delete(p.id)
