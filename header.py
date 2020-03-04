from flask import Flask, request, abort
from functools import wraps

app = Flask(__name__)

def get_token_auth_header():
    if 'Authorization' not in request.headers:
        abort(401)
    
    headers = request.headers['Authorization'].split(' ')
    
    if len(headers) != 2:
        abort(401)

    if headers[0].lower() != 'bearer':
        abort(401)

    return headers[1]

# Lets make a wrapper! My first
def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(get_token_auth_header(), *args, **kwargs)
    return wrapper

# jwt is get_token_auth_header() passed through wrapper
@app.route('/headers')
@requires_auth
def get_headers(jwt):
    return jwt