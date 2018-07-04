import os
import dns.resolver

from flask import Flask

# create and configure the app
app = Flask(__name__, instance_relative_config=True)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/resolve/<domain>')
def resolve(domain):
    result = dns.resolver.query(domain, 'A')
    ips = [str(ip) for ip in result]
    app.logger.error(repr(result) + 'length: %s', len(ips))
    return 'resolving %s...<br/>' % domain + '<br/>'.join(ips)
