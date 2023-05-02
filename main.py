from flask import Flask
from flask import request, jsonify
from action import Action
import time
import random
import hashlib

app = Flask(__name__)
ac = Action()

def token_assert(token):
    return len(token) == 16

@app.route('/')
def index():
    return 'PASCC-BACKEND'

@app.route('/register')
def register():
    tstp = str(int(time.time()) * 1000000)
    host = str(request.host_url)
    randi = random.randint(10000000,99999999)
    stamp = tstp + host + str(randi)
    # md5
    token = hashlib.md5(stamp.encode('utf-8')).hexdigest()[8:24]
    return jsonify({'status': 0, 'token': token})
    


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    token = str(data['token'])

    if not token_assert(token):
        return jsonify({'status': 3, 'msg': 'token error', 'result':'', 'output':''})
    
    source = str(data['source'])
    runflag = bool(data['runflag'])
    try:
        rcode, res, out = ac.run(token, source, runflag)
    except Exception as e:
        rcode = -1
        res = str(e)
        out = ''
        
    return jsonify({'status': rcode, 'msg': 'message', 'result':res, 'output':out})
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)