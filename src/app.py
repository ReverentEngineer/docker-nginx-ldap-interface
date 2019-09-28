from flask import Flask, request, Response
from base64 import b64decode
import ldap
from os import environ

app = Flask(__name__)
app.config['LDAP_URI'] =  environ.get("LDAP_URI", default="ldap://localhost")
app.config['LDAP_BIND_TEMPLATE'] = environ.get("LDAP_BIND_TEMPLATE", default="%s")

def check(authorization_header):
    try:
        authtype, authdata = authorization_header.split(" ")
        if authtype != 'Basic':
            return False
        username, password = b64decode(authdata).decode("utf-8").split(":")
    except Exception as e:
        app.logger.warn("Invalid authorization format: %s" % str(e))
        return False

    try:
        conn = ldap.initialize(app.config['LDAP_URI'])
        conn.simple_bind_s(app.config['LDAP_BIND_TEMPLATE'] % (username), password)
        app.logger.info('%s logged in successfully.', username)
        conn.unbind()
        return True
    except Exception as e:
        app.logger.warn('Failed log in attempt: %s', str(e))
        return False

@app.route('/auth')
def confidential():
    authorization_header = request.headers.get('Authorization')
    if authorization_header and check(authorization_header):
        return "Authorized", 200
    else:
        response = Response()
        response.headers['WWW-Authenticate'] = 'Basic'
        return response, 401
