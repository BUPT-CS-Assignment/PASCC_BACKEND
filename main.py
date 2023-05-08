from flask import Flask
from flask import request, jsonify
from action import Action
import time
import random
import hashlib

app = Flask(__name__)
ac = Action()

cors = [('Access-Control-Allow-Origin','*'),
        ('Access-Control-Allow-Methods','GET, HEAD, POST, OPTIONS'),
        ('Access-Control-Allow-Headers','content-type')]

def token_assert(token):
    return len(token) == 16

@app.route('/', methods=['GET'])
def index():
    return 'PASCC-BACKEND'

@app.route('/register', methods=['GET'])
def register():
    tstp = str(int(time.time()) * 1000000)
    host = str(request.host_url)
    randi = random.randint(10000000,99999999)
    stamp = tstp + host + str(randi)
    # md5
    token = hashlib.md5(stamp.encode('utf-8')).hexdigest()[8:24]
    return (jsonify({'status': 0, 'token': token}),200,cors)
    


@app.route('/submit', methods=['POST','OPTIONS'])
def submit():
    if request.method == 'OPTIONS':
        return ('',200,cors)
    data = request.get_json()
    token = str(data['token'])

    if not token_assert(token):
        return (jsonify({'status': 3, 'msg': 'token error', 'result':'', 'output':''}),401,cors)
    
    source = str(data['source'])
    runflag = bool(data['runflag'])
    try:
        rcode, res, out = ac.run(token, source, runflag)
    except Exception as e:
        rcode = -1
        res = str(e)
        out = ''
        
    return (jsonify({'status': rcode, 'msg': 'message', 'result':res, 'output':out}),200,cors)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10443, debug=True, ssl_context=('/home/jianxf/.https/api.pem','/home/jianxf/.https/api.key'))