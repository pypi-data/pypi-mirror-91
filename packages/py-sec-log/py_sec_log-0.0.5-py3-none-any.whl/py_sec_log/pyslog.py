import requests, os, sys
from licensing import methods
from licensing.methods import Helpers
import hashlib
class login:
    k=Helpers.GetMachineCode()
    ke=k.encode('utf-8')
    ey=hashlib.md5(ke)
    global key
    key=ey.hexdigest()
    def user_id():
        print(Helpers.GetMachineCode())
    def auth(auth_id):
        if auth_id=='':
            print('Please Enter auth_id')
            sys.exit()
        else:
            global r
        r=requests.get('https://pastebin.com/'+auth_id)
    def verify(username, password):
        if username=='' and password=='' or username=='' or password=='':
            print('Need Username And Password For Login!')
            sys.exit()
        else:
            pass
        ins=username+password
        sec=ins.encode('utf-8')
        secu=hashlib.md5(sec)
        info=secu.hexdigest()
        if info in r.text:
            if key in r.text:
                pass
            else:
                print('Unexpected Error!')
                sys.exit()
        else:
            print('Invalid Username Or Password!')
            sys.exit()
