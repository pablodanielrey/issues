import os
import requests
import inspect

from jinja2 import Environment, FileSystemLoader
from redminelib import Redmine


class UsersAPI:

    USERS_API_URL = os.environ['USERS_API_URL']

    @classmethod
    def obtenerInfoUsuario(cls, uid):
        r = requests.get(cls.USERS_API_URL + '/usuarios/' + uid)
        return r.json()



class IssuesModel:

    TEMPLATES = None
    URL = os.environ['ISSUES_REDMINE_URL']
    KEY = os.environ['ISSUES_REDMINE_KEY']
    GUID_ERROR_SISTEMAS = '7528373b-2492-4428-9cd9-689ef5b04631'
    GUID_PEDIDO_MANTENIMIENTO = '8407abb2-33c2-46e7-bef6-d00bab573306'
    GUID_PEDIDO_ADMINISTRATIVA = 'secretaria-administrativa'
    GUID_PEDIDO_DITESI = '117ae745-acb3-48df-9005-343538f85403'

    @classmethod
    def _formatear(cls, persona, contacto, pedido, template):
        if not cls.TEMPLATES:
            cls.TEMPLATES = os.path.dirname(inspect.getfile(cls)) + '/templates'
        env = Environment(loader=FileSystemLoader(cls.TEMPLATES), trim_blocks=False)
        templ = env.get_template(template)
        return templ.render(persona=persona, contacto=contacto, pedido=pedido)

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
        user_id = None
        for u in r.user.filter(name=usuario['dni']):
            break
        else:
            user_id = cls.crear_usuario_redmine(r, usuario)
        return


    # ------ pedidos a oficinas -----

    @classmethod
    def _crear_pedido_a_oficina(cls, uid, contacto, pedido, template, GUID):
        usuario = UsersAPI.obtenerInfoUsuario(uid)

        sub = '{} - {} - {} - {} - {}...'.format(usuario['dni'], usuario['nombre'], usuario['apellido'], contacto['correo'], pedido[:20])
        cuerpo = cls._formatear(usuario, contacto, pedido, template)

        cls.crear_usuario_redmine_si_no_existe(usuario)
        r = Redmine(cls.URL, key = cls.KEY, version='3.3', impersonate=usuario['dni'], requests={'verify': False})
        pedidos = r.project.get(GUID)

        issue = r.issue.new()
        issue.project_id = pedidos.id
        issue.subject = sub
        issue.description = cuerpo
        issue.save()

        return issue.id


    @classmethod
    def crear_pedido_mantenimiento(cls, uid, contacto, pedido):
        return cls._crear_pedido_a_oficina(uid, contacto, pedido, 'pedido_mantenimiento.tmpl', cls.GUID_PEDIDO_MANTENIMIENTO)

    @classmethod
    def crear_pedido_administrativa(cls, uid, contacto, pedido):
        return cls._crear_pedido_a_oficina(uid, contacto, pedido, 'pedido_administrativa.tmpl', cls.GUID_PEDIDO_ADMINISTRATIVA)

    @classmethod
    def crear_pedido_ditesi(cls, uid, contacto, pedido):
        return cls._crear_pedido_a_oficina(uid, contacto, pedido, 'pedido_ditesi.tmpl', cls.GUID_PEDIDO_DITESI)



    # ---------------------- reporte de errores de los sistemas implementados --------------------------

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
