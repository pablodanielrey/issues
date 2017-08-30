from functools import wraps
from flask import Flask, request, send_from_directory, g, redirect, make_response
from flask_httpauth import HTTPBasicAuth

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/src/issues/web/angular')
auth = HTTPBasicAuth()

def redirect_not_authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        app.logger.debug('redirect_not_authenticated {}'.format(g.authenticated))
        if not g.authenticated:
            app.logger.debug('no')
            """
                1 - generar un hash temporal

                hash = generate_hash()

                2 - enviar al login ese hash + referer (request.url) para ser procesado

                login.api.wamp.internal_hash(hash, referer, timeout)

                3 - retornar al cliente un redirect al login + parametro = hash

                return redirect("http://login.econo.unlp.edu.ar?t={}".format(hash), code=302)
            """
            token = 'dfsdfd'
            return redirect("http://login.econo.unlp.edu.ar?t={}".format(token), code=302)
        else:
            if g.authenticated == 'algo':
                return make_response(request.url, 200)
            else:
                app.logger.debug('yes')
                resp = make_response(redirect("/index"))
                resp.set_cookie('token', value='algo')
                return resp
                """ return f(*args, **kwargs) """
    return decorated

@auth.verify_password
def verify_password(username, password):
    app.logger.debug('verify_password {}'.format(username))

    """ chequeo si existe la cookie token """
    t = request.cookies.get('token')
    if t:
        g.authenticated = t
        return True

    """ chequeo info de usuario """
    if username == '':
        g.authenticated = False
        return False
    else:
        g.authenticated = username
    return True


@app.route('/')
@auth.login_required
@redirect_not_authenticated
def sendRoot():
    return send('/')

@app.route('/<path:path>')
@auth.login_required
@redirect_not_authenticated
def send(path):
    app.logger.debug('send')
    return send_from_directory(app.static_url_path, path)


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == "__main__":
    main()
