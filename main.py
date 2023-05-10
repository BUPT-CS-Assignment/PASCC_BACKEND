from flask import Flask
from flask import request, jsonify
from action import Action
import time
import random
import hashlib
import subprocess
import datetime
from pypushdeer import PushDeer
import threading

pushdeer = PushDeer(pushkey="PDU15463TwaXIVKELKXUAdLKoQ741xDaNtYlJzgSO")
app = Flask(__name__)
ac = Action()

cors = [('Access-Control-Allow-Origin','*'),
        ('Access-Control-Allow-Methods','GET, HEAD, POST, OPTIONS'),
        ('Access-Control-Allow-Headers','content-type')]

def token_assert(token):
    return len(token) == 18

@app.route('/', methods=['GET'])
def index():
    return 'PASCC-BACKEND'

@app.route('/register', methods=['GET'])
def register():
    tstp = str(int(time.time() * 1000000))

    host = str(request.host_url)
    randi = random.randint(10000000,99999999)
    stamp = tstp + host + str(randi)
    # md5
    token = tstp[0:10] + hashlib.md5(stamp.encode('utf-8')).hexdigest()[8:16]
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

@app.route('/feedback',methods=['POST','OPTIONS'])
def feedback():
    if request.method == 'OPTIONS':
        return ('',200,cors)
    data = request.get_json()
    token = str(data['token'])

    if not token_assert(token):
        return (jsonify({'status': 3, 'msg': 'token error'}),401,cors)
    
    text = str(data['text'])
    try:
        pushdeer.send_text(text)
        status = 0
        msg = 'feedback success'
    except Exception as e:
        print(e)
        status = 2
        msg = str(e)
    return (jsonify({'status':status, 'msg':msg}),200,cors)
    

@app.route('/update',methods=['POST','OPTIONS'])
def update():
    if request.method == 'OPTIONS':
        return ('',200,cors)
    
    # authentic
    data = request.get_json()
    try:
        if data["repository"]["owner"]['login'] != "PASCC-TEAM":
            return 'Authentic Failed',401
    except Exception:
        return "Authentic Failed",401

    # fetch
    p = subprocess.Popen('/home/jianxf/Service/PASCC_BACKEND/update.sh',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = p.communicate()

    # log
    date = datetime.datetime.now().strftime('%Y%m%d')
    with open('./logs/' + date + '.log','a+') as f:
        f.write(str('update on ' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + '\n')
        if err: 
            f.write(str(err)+'\n')
        
    try:
        thread = threading.Thread(target=make_)
        thread.start()
    except Exception as e:
        print(str(e))
    return 'update success',200

def make_():
    p = subprocess.Popen('/home/jianxf/Service/PASCC_BACKEND/make.sh',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = p.communicate()

    # log
    date = datetime.datetime.now().strftime('%Y%m%d')
    with open('./logs/' + date + '.log','a+') as f:
        f.write(str('update on ' + datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + '\n')
        if err: f.write(str(err)+'\n')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10443, debug=True, ssl_context=('/home/jianxf/.https/api.pem','/home/jianxf/.https/api.key'))
