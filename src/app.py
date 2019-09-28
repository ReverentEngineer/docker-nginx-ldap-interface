from flask import Flask, request, Response
from base64 import b64decode
import ldap
from os import environ

app = Flask(__name__)
app.config['LDAP_URI'] =  environ.get("LDAP_URI", default="ldap://localhost")
app.config['LDAP_BIND_TEMPLATE'] = environ.get("LDAP_BIND_TEMPLATE", default="%s")

def parse_basic_auth():
    auth_header = request.headers.get('Authorization')
    authtype, authdata = auth_header.split(" ")
    if authtype != 'Basic':
        raise Exception('Invalid authorization type.')  
    return b64decode(authdata).decode("utf-8").split(":")

def check(username, password):
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
def auth():
    try:
        username, password = get_basic_auth()
        response = Response()
        if check(username, password):
            response.headers['X-Username'] = username
            return response, 200
        else:
            response.headers['WWW-Authenticate'] = 'Basic'
            return response, 401
    except:
        app.logger.warn('Problem processing request: %s', str(e))
        return "Bad Request", 400
