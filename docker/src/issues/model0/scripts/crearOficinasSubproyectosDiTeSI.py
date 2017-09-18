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

    #los ids de las oficinas generadas son: dId_idDeLaOficina
    #asi que se puede separar los ids usando split('_')

    con = psycopg2.connect(
                    host=os.environ['ISSUES_DB_HOST'],
                    dbname=os.environ['ISSUES_DB_NAME'],
                    user=os.environ['ISSUES_DB_USER'],
                    password=os.environ['ISSUES_DB_PASSWORD'])

    try:
        cur = con.cursor()
        try:
            params = (('center', 'direction', 'institute', 'secretary', 'unity'),)
            cur.execute('select id, name, type from offices.offices where removed is null and type in %s', params)
            for o in cur:
                oid = dId + '_' + o[0]

                try:
                    r.project.get(oid)

                except ResourceNotFoundError:
                    name = o[1] if o[1] else ''
                    otype = o[2] if o[2] else ''
                    p = r.project.create(
                        name=name,
                        identifier=oid,
                        description=otype,
                        is_public=True,
                        parent_id=pId,
                        inherit_members=True
                    )
                    logging.info('proyecto creado: {}'.format(p))

        finally:
            cur.close()

    finally:
        con.close()
