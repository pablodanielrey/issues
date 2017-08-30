import logging
logging.basicConfig(level=logging.DEBUG)

import os


'''
    escribo el archivo de propiedades de oidc desde las propiedades del environment
'''
with open('/tmp/client_secrets.json','w') as f:
    import json
    json.dump({"web": {
      "client_id":"some-consumer",
      "client_secret":"consumer-secret",
      "auth_uri": os.environ['LOGIN_OIDC_URL'] + "/authorization",
      "token_uri": os.environ['LOGIN_OIDC_URL'] + "/token",
      "userinfo_uri": os.environ['LOGIN_OIDC_URL'] + "/userinfo",
      "issuer": os.environ['LOGIN_OIDC_ISSUER'],
      "redirect_uris": os.environ['ISSUES_URL'] + "/oidc_callback"
    }}, f)



import flask
from flask import Flask, request, send_from_directory, jsonify, redirect, url_for
from flask_jsontools import jsonapi
#from flask_oidc import OpenIDConnect
from auth_utils import MyOpenIDConnect, DictWrapper

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/src/users/web')
app.debug = True
app.config['SECRET_KEY'] = 'algo-secreto'
app.config['SESSION_COOKIE_NAME'] = 'users_session'

app.config['OIDC_CLIENT_SECRETS'] = '/tmp/client_secrets.json'
app.config['OIDC_COOKIE_SECURE'] = False
app.config['OIDC_VALID_ISSUERS'] = [os.environ['LOGIN_OIDC_ISSUER']]
app.config['OIDC_RESOURCE_CHECK_AUD'] = False
app.config['OIDC_INTROSPECTION_AUTH_METHOD'] = 'client_secret_post'
app.config['OIDC_ID_TOKEN_COOKIE_NAME'] = 'users_oidc'
app.config['OIDC_USER_INFO_ENABLED'] = True
app.config['OIDC_SCOPES'] = ['openid','email','phone','profile','address','econo']

oidc = MyOpenIDConnect(app, credentials_store=DictWrapper('credentials_store'))

@app.route('/config.json', methods=['GET'])
@oidc.require_login
@jsonapi
def configuracion():
    #usuario = oidc.user_getinfo(['sub','name','family_name','picture','email','email_verified','birdthdate','address','profile','econo'])
    usuario = oidc.user_getinfo()
    return {
        'usuario': usuario,
        'issues_api_url': os.environ['ISSUES_API_URL']
    }

@app.route('/logout', methods=['GET'])
@oidc.require_login
def logout():
    oidc.logout()
    return redirect(url_for('send'))

@app.route('/libs/<path:path>', methods=['GET'])
def send_libs(path):
    return send_from_directory(app.static_url_path + '/libs', path)


@app.route('/', methods=['GET'], defaults={'path':None})
@app.route('/<path:path>', methods=['GET'])
@oidc.require_login
def send(path):
    if not path:
        return redirect('/index.html'), 303
    return send_from_directory(app.static_url_path, path)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

def main():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()
