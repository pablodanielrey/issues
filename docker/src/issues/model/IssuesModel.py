import os
import requests

from redminelib import Redmine


class UsersAPI:

    USERS_API_URL = os.environ['USERS_API_URL']

    @classmethod
    def obtenerInfoUsuario(cls, uid):
        r = requests.get(cls.USERS_API_URL + '/usuarios/' + uid)
        return r.json()



class IssuesModel:

    URL = os.environ['ISSUES_REDMINE_URL']
    KEY = os.environ['ISSUES_REDMINE_KEY']
    GUID = '7528373b-2492-4428-9cd9-689ef5b04631'

    @classmethod
    def crear_usuario_redmine(r, usuario):
        user = redmine.user.new()
        user.login = usuario['dni']
        user.password = 'nada por ahora'
        user.firstname = usuario['nombre']
        user.lastname = usuario['apellido']
        user.mail = 'autogenerado@econo.unlp.edu.ar'
        user.save()
        return user.id

    @classmethod
    def crear_usuario_redmine_si_no_existe(cls, usuario):
        r = Redmine(cls.URL, key = cls.KEY, version='3.3', requests={'verify': False})
        pedidos = r.project.get(cls.GUID)

        user_id = None
        for u in r.user.filter(name=usuario['dni']):
            break
        else:
            user_id = cls.crear_usuario_redmine(r, usuario)
        return


    @classmethod
    def crear_pedido_ditesi_privado(cls, persona, problema):

        uid = persona['id']
        usuario = UsersAPI.obtenerInfoUsuario(uid)

        sub = '{} - {} - {} - {}'.format(usuario['dni'], usuario['nombre'], usuario['apellido'], persona['correo'])
        desc = '''
            DNI:        {}
            Nombre:     {}
            Apellido:   {}
            Telefono:   {}
            Correo:     {}
            Problema:

            {}
        '''.format(usuario['dni'], usuario['nombre'], usuario['apellido'], persona['telefono'], persona['correo'], problema)


        cls.crear_usuario_redmine_si_no_existe(usuario)
        r = Redmine(cls.URL, key = cls.KEY, version='3.3', impersonate=usuario['dni'], requests={'verify': False})
        pedidos = r.project.get(cls.GUID)

        issue = r.issue.new()
        issue.project_id = pedidos.id
        issue.subject = sub
        issue.description = desc
        issue.save()

        return issue.id


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
