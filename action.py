import os
import datetime
import subprocess

class Action:
  def __init__(self):
    pass

  def run_(self,input:str, output:str, if_run:bool, args:str=''):
    cmd = './assets/PASCC -d 2 -i ' + input + ' -o ' + output

    if if_run:
      cmd += ' -t '
      cmd += '"'+args+'"'

    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding='utf-8')
    try:
      out,err = p.communicate(input=None,timeout=3)
      status = p.returncode
      out = str(out) if out != None else ''
      err = str(err).replace('\u001b[0m','').replace('\u001b[01;31m','').replace('\033[01;32m','')
    except subprocess.TimeoutExpired:
      p.kill()
      out = ''
      err = 'subprocess.TimeoutExpired'
      status = 2

    date = datetime.datetime.now().strftime('%Y%m%d')

    with open('./logs/' + date + '.log','a+') as f:
      f.write(out)

    return status,err


  def run(self,token,source:str,run_flag:bool):

    input = './tmp/' + token + '.pas'
    output = './tmp/' + token + '.c'
    result = './tmp/' + token + '.txt'

    with open(input,'w') as f:
      f.write(source)
    
    status,err = self.run_(input,output,run_flag,'> ' + result)
    c_code = 'Internal Error.'
    run_res = ''

    if status == 2:
      c_code = 'program running exceed 3 seconds.'
    elif status == 1:
      c_code=str(err)
    elif status == 0:
      if run_flag:
        with open(result,'r') as f: run_res = f.read()
        os.remove(result)  

      with open(output,'r') as f: c_code = f.read()
      os.remove(output)

      
      

    return status, c_code, run_res  





    