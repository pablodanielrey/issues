import os
from redminelib import Redmine

class IssuesModel:

    URL = os.environ['ISSUES_REDMINE_URL']
    KEY = os.environ['ISSUES_REDMINE_KEY']
    GUID = '7528373b-2492-4428-9cd9-689ef5b04631'

    @classmethod
    def crear_pedido_ditesi_publico(cls, persona, problema):

        sub = '{} - {} - {} - {}'.format(persona['dni'], persona['nombre'], persona['apellido'], persona['correo'])
        desc = '''
            DNI:        {}
            Nombre:     {}
            Apellido:   {}
            Telefono:   {}
            Correo:     {}
            Problema:

            {}
        '''.format(persona['dni'], persona['nombre'], persona['apellido'], persona['telefono'], persona['correo'], problema)



        r = Redmine(cls.URL, key = cls.KEY, version='3.3', requests={'verify': False})
        pedidos = r.project.get(cls.GUID)

        issue = r.issue.new()
        issue.project_id = pedidos.id
        issue.subject = sub
        issue.description = desc
        issue.save()

        return issue.id
