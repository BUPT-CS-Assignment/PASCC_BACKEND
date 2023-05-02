import os
import datetime
import subprocess

class Action:
  __env = 0 # 0: Windows, 1: Linux

  def __init__(self):
    self.__env = 0

  def set_win64(self):
    self.__env = 0

  def set_linux(self):
    self.__env = 1

  def run_(self,input:str, output:str, if_run:bool, args:str=''):
    if self.__env == 0:
      cmd = 'assets\\PASCC.exe -d 2 -i '+input+' -o '+output
    else:
      cmd = 'assets/PASCC -d 2 -i '+input+' -o '+output

    if if_run:
      cmd += ' -t '
      cmd += args

    # out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    out = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,encoding='utf-8')
    try:
      log = out.communicate(input=None,timeout=1)[0]
      ret_code = out.returncode
    except subprocess.TimeoutExpired:
      out.kill()
      log = 'subprocess.TimeoutExpired'
      ret_code = 2

    date = datetime.datetime.now().strftime('%Y%m%d')
    div = '/' if self.__env == 1 else '\\'
    with open('logs' + div + date + '.log','a+') as f:
      f.write(log)

    return ret_code


  def run(self,token,source:str,run_flag:bool):
    div = '/' if self.__env == 1 else '\\'
    input = 'tmp' + div + token + '.pas'
    output = 'tmp' + div + token + '.c'
    result = 'tmp' + div + token + '.txt'

    with open(input,'w') as f:
      f.write(source)
    rcode = self.run_(input,output,run_flag,'> ' + result)
    print(rcode)
    if rcode == 2:
      ret_code = 'program running exceed 1 seconds.'
      ret_result = ''
    elif rcode == 1:
      ret_code = 'Syntax Error.'
      ret_result = ''
    else:
      if run_flag:
        with open(result,'r') as f:
          ret_result = f.read()
        os.remove(result)  
      else:
        ret_result = ''

      with open(output,'r') as f:
        ret_code = f.read()

    # os.remove(input)
    # os.remove(output)
    return rcode, ret_code, ret_result  





    