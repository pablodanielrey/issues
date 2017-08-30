import logging
from flask_oidc import OpenIDConnect

logger = logging.getLogger(__name__)

class MyOpenIDConnect(OpenIDConnect):
    '''
        Reemplaza métodos que funcionan mal o fuera de la especificación
    '''
    def __init__(self, app, credentials_store=None):
        super().__init__(app, credentials_store)
        self.current_app = app


    def user_getinfo(self, fields=None, access_token=None):
        """
        Request multiple fields of information about the user.

        :param fields: The names of the fields requested.
        :type fields: list
        :returns: The values of the current user for the fields requested.
            The keys are the field names, values are the values of the
            fields as indicated by the OpenID Provider. Note that fields
            that were not provided by the Provider are absent.
        :rtype: dict
        :raises Exception: If the user was not authenticated. Check this with
            user_loggedin.

        .. versionadded:: 1.0
        """
        from flask import g


        if g.oidc_id_token is None and access_token is None:
            raise Exception('User was not authenticated')
        info = {}
        all_info = None

        ''' ----------------------- parche mío para agregar que retorne toda la info que tenga cuando fields == None ------------------- '''
        if not fields:
            import copy
            info = copy.deepcopy(g.oidc_id_token)
            if self.current_app.config['OIDC_USER_INFO_ENABLED']:
                all_info = self._retrieve_userinfo(access_token)
                for f in all_info:
                    info[f] = all_info[f]
        else:
            for field in fields:
                if access_token is None and field in g.oidc_id_token:
                    info[field] = g.oidc_id_token[field]
                elif self.current_app.config['OIDC_USER_INFO_ENABLED']:
                    # This was not in the id_token. Let's get user information
                    if all_info is None:
                        all_info = self._retrieve_userinfo(access_token)
                        if all_info is None:
                            # To make sure we don't retry for every field
                            all_info = {}
                    if field in all_info:
                        info[field] = all_info[field]
                    else:
                        # We didn't get this information
                        pass
        return info

    def _is_id_token_valid(self, id_token):
        '''
        Check if `id_token` is a current ID token for this application,
        was issued by the Apps domain we expected,
        and that the email address has been verified.
        @see: http://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation
        '''
        if not id_token:
            return False

        import time

        # step 2: check issuer
        if id_token['iss'] not in self.current_app.config['OIDC_VALID_ISSUERS']:
            logger.error('id_token issued by non-trusted issuer: %s' % id_token['iss'])
            return False

        if isinstance(id_token['aud'], list):
            # step 3 for audience list
            if self.flow.client_id not in id_token['aud']:
                logger.error('We are not a valid audience')
                return False

            if len(id_token['aud']) > 1:
                # step 4
                if 'azp' not in id_token:
                    logger.error('Multiple audiences and not authorized party')
                    return False
        else:
            # step 3 for single audience
            if id_token['aud'] != self.flow.client_id:
                logger.error('We are not the audience')
                return False

       # step 5
        if 'azp' in id_token and id_token['azp'] != self.flow.client_id:
            logger.error('Authorized Party is not us')
            return False

        # step 6-8: TLS checked

        # step 9: check exp
        if int(time.time()) >= int(id_token['exp']):
            logger.error('Token has expired')
            return False

        # step 10: check iat
        if id_token['iat'] < (time.time() - self.current_app.config['OIDC_CLOCK_SKEW']):
            logger.error('Token issued in the past')
            return False

        # (not required if using HTTPS?) step 11: check nonce
        # step 12-13: not requested acr or auth_time, so not needed to test

        # additional steps specific to our usage
        if self.current_app.config['OIDC_GOOGLE_APPS_DOMAIN'] and id_token.get('hd') != self.current_app.config['OIDC_GOOGLE_APPS_DOMAIN']:
            logger.error('Invalid google apps domain')
            return False

        if not id_token.get('email_verified', False) and self.current_app.config['OIDC_REQUIRE_VERIFIED_EMAIL']:
            logger.error('Email not verified')
            return False

        return True


class DictWrapper(object):
    def __init__(self, name, d=None):
        self.name = name
        if d:
            self.data = dict(d)
        else:
            self.data = dict()

    def __setitem__(self, key, value):
        logging.debug('{} --- setitem {} --> {}'.format(self.name, key, value))
        self.data[key] = value

    def __getitem__(self, key):
        v = self.data[key]
        logging.debug('{} --- getitem {} --> {}'.format(self.name, key, v))
        return v

    def __delitem__(self, key):
        logging.debug('{} --- delitem {}'.format(self.name, key))
        del self.data[key]

    def __contains__(self, key):
        logging.debug('{} --- contains {}'.format(self.name, key))
        return key in self.data

    def items(self):
        logging.debug('{} ---  items --'.format(self.name))
        return self.data.items()

    def pop(self, key, default=None):
        v = self.data.pop(key)
        logging.debug('{} --- pop {} --> {}'.format(self.name, key, v))
        return v

__all__ = [
    'MyOpenIDConnect',
    'DictWrapper'
]
