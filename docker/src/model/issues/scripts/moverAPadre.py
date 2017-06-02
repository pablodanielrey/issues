import logging
import os
import sys
from redmine import Redmine

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    r = Redmine(os.environ['ISSUES_REDMINE_URL'], key = os.environ['ISSUES_REDMINE_KEY'], version='3.3', requests={'verify': False})

    pid = sys.argv[1]

    pParent = pid
    pd = r.project.get(pParent)

    print('Esta seguro que desea mover las tareas de los subproyectos de {}'.format(pd))
    input('Presione una tecla para continual ...')

    """ transformar los subtareas en entradas en el journal """
    issues = r.issue.filter(project_id=pd.id, subproject_id='*', status_id = '*')
    for i in issues:
        if i.project.id != pd.id:
            logging.info('Moviendo {} de {} a {}'.format(i.id, i.project, pd))
            i.project_id = pd.id
            i.save()
