# -*- coding: utf-8 -*-

#from model.users.users  import UserPassword, User, Mail
#from model.offices.office import Office
#from model.serializer import JSONSerializable
#from model.registry import Registry
import base64
import logging
import datetime
import uuid
import re
#from model.assistance.utils import Utils
from issues.model import Issues
from issues.model import UserIssueData
from issues.model.RedmineAPI import RedmineAPI

"""
import cProfile

def do_cprofile(func):
    def profiled_func(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats()
    return profiled_func
"""



class IssuesModel():
    TRACKER_ERROR = RedmineAPI.TRACKER_ERROR
    TRACKER_COMMENT = RedmineAPI.TRACKER_COMMENT
    cache = {}
    ditesiId = '117ae745-acb3-48df-9005-343538f85403'
    soporteId = '4a3409e3-b4f0-43ab-b922-98a1138e3360'
    desarroloId = 'e55e67d4-9675-4bdf-bed0-da3adc0aec71'
    servidoresId = '02ad99c8-934d-402b-ab3e-64fd2440de05'

    @classmethod
    def getSubjectTypes(cls, con, oId):
        generic = [
            'Quiero una cuenta institucional de correo',
            'No tengo usuario y clave',
            'No me acuerdo mi usuario/clave',
            'Ingreso mi clave pero me dice acceso denegado/incorrecto',
            'No tengo acceso a internet',
            'No puedo enviar correo',
            'No puedo recibir correo',
            'Envié correo y no llega a destino',
            'Me enviaron correo y no lo recibo',
            'Tengo problemas con la libreta de direcciones'
        ]
        systems = [
            'No puedo entrar al sistema',
            'No puedo entrar al au24',
            'No funciona el sistema de Asistencia',
            'No funciona el sistema de Pedidos',
            'No funciona el sistema de Inserción Laboral',
            'No puedo actualizar mis datos',
            'No puedo subir mi CV',
            'Error en el sistema'
        ]
        net = [
            'No me puedo conectar a la wifi',
            'Estoy conectado a wifi pero no navega'
        ]
        supp = [
            'El equipo no enciende',
            'El equipo anda lento',
            'El equipo hace mucho ruido',
            'El equipo se apaga solo',
            'Error de Windows o Programas',
            'Problemas con Monitor',
            'No encuentro un archivo',
            'Problemas con la nube (archivos)',
            'Me quede sin espacio en disco',
            'No puedo imprimir',
            'Problemas con la impresora',
            'Virus',
            'Problema de perfil de usuario'
        ]
        if oId == cls.ditesiId:
            r = []
            r.extend(generic)
            r.extend(systems)
            r.extend(net)
            r.extend(supp)
            r.append('Otro')
            return r
        elif oId == cls.soporteId:
            r = []
            r.extend(generic)
            r.extend(net)
            r.extend(supp)
            r.append('Otro')
            return r
        elif oId == cls.desarroloId:
            r = []
            r.extend(systems)
            r.append('Otro')
            return r
        elif oId == cls.servidoresId:
            r = []
            r.extend(generic)
            r.extend(systems)
            r.extend(net)
            r.append('Otro')
            return r
        else:
            return ['Otro']

    @classmethod
    def getOffices(cls, con, userId):
        """
            retorna las oficinas públicas que están permitidas como destino de pedidos.
            oficinas públicas.
            suboficinas de las oficinas a la que pertenece la persona (tipo: direcciones y departamentos).
        """
        officesIds = Office.findAll(con)
        projects = RedmineAPI.findAllProjects()
        offices = Office.findByIds(con, [oid for oid in officesIds if oid in projects])
        publicOffices = [o for o in offices if o.public]

        userOfficesIds = Office.findByUser(con, userId, types=['direction','department'], tree=True)
        userOffices = Office.findByIds(con, [oid for oid in userOfficesIds if oid in projects])

        if userOffices is not None:
            idPublicOffices = [o.id for o in publicOffices]
            publicOffices.extend([o for o in userOffices if o.id not in idPublicOffices])

        return publicOffices

    @classmethod
    def getAreas(cls, con, oId):
        """
            Retorna las suboficinas de oId que tienen tipo área.
            También se les puede realizar pedidos a las áreas específicas.
        """
        offs = Office.findByIds(con, [oId])
        if offs is None or len(offs) <= 0:
            return []
        areas = offs[0].findChilds(con, types=['area'], tree=False)
        return Office.findByIds(con, areas)

    @classmethod
    def create(cls, con, parentId, officeId, authorId, subject, description, fromOfficeId, creatorId, files, tracker = TRACKER_ERROR):
        issue = Issues()
        issue.parentId = parentId
        issue.projectId = officeId
        issue.userId = authorId
        issue.subject = subject
        issue.description = description
        issue.tracker = tracker
        issue.fromOfficeId = fromOfficeId
        issue.creatorId = creatorId


        issue.files = []
        for file in files:
            data = base64.b64decode(file['content'])
            id = str(uuid.uuid4())
            path = '/tmp/' + id
            f = open(path, 'wb')
            f.write(data)
            f.close()
            issue.files.append({'path':path, 'filename':file['name'], 'content_type': file['type']})

        return issue.create(con)

    @classmethod
    def searchUsers(cls, con, regex):
        assert regex is not None

        if regex == '':
            return []

        userIds = User.search(con, regex)

        users = []
        for u in userIds:
            (uid, version) = u
            if uid not in cls.cache.keys():
                print(uid)
                user = User.findById(con, [uid])[0]
                cls.cache[uid] = user
            users.append(cls.cache[uid])

        """
            antes de implementar el search en users se usaba esto.
        m = re.compile(".*{}.*".format(regex), re.I)
        matched = []

        digits = re.compile('^\d+$')
        if digits.match(regex):
            ''' busco por dni '''
            matched = [ cls._getUserData(con, u) for u in users if m.search(u.dni) ]
            return matched

        ''' busco por nombre y apellido '''
        matched = [ cls._getUserData(con, u) for u in users if m.search(u.name) or m.search(u.lastname) ]
        return matched
        """

        return [cls._getUserData(con, u) for u in users]



    @classmethod
    def _getUserData(cls, con, user):
        u = UserIssueData()
        u.name = user.name
        u.lastname = user.lastname
        u.dni = user.dni
        u.id = user.id
        u.genre = user.genre
        u.photo = [User.findPhoto(con, user.photo) if 'photo' in dir(user) and user.photo is not None and user.photo != '' else None][0]
        return u
