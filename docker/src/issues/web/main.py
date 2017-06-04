from functools import wraps
from flask import Flask, request, send_from_directory, g, redirect
from flask_httpauth import HTTPBasicAuth

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='/src/issues/web/angular')
auth = HTTPBasicAuth()

def redirect_not_authenticated(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        app.logger.debug('redirect_not_authenticated')
        if not g.authenticated:
            app.logger.debug('no')
            return redirect("http://login.econo.unlp.edu.ar", code=302)
        else:
            app.logger.debug('yes')
            return f(*args, **kwargs)
    return decorated

@auth.verify_password
def verify_password(username, password):
    app.logger.debug('verify_password {}'.format(username))
    if username == '':
        g.authenticated = False
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
