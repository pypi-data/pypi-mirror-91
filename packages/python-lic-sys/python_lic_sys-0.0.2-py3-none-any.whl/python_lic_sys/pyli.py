#*Coding UTF_8*#
#Author: TechSmit#
from licensing import methods
from licensing.methods import Helpers
import hashlib
import base64
import os, sys, requests
        
class slab:
    @staticmethod
    def auth(auth_id):
        if auth_id=="":
            print('Please Enter Authentication id For Verification!')
            sys.exit()
        global r
        r=('https://pastebin.com/'+auth_id)
class userid:
    @staticmethod
    def user_id():
        print('USER ID:'+Helpers.GetMachineCode())
class license:
    @staticmethod
    def verify(username, password, key):
        try:
            req=requests.get(r)
            #r=requests.get('https://pastebin.com/'+auth_id)
            ke=Helpers.GetMachineCode()
            co=ke.encode('utf-8')
            k=hashlib.md5(co)
            e=k.hexdigest()
            KEY=e.upper()
            info=username+'\n'+password
            ok=info.encode('utf-8')
            say=hashlib.md5(ok)
            h=say.hexdigest()
            if h in r.text:
                if key==KEY:
                    if e in req.text:
                        pass
                    else:
                        print('Invalid Account')
                        sys.exit()
                else:
                    print('Please Use Your Device Or Key!')
                    sys.exit()
            else:
                print('Invalid Username Or Password!')
                sys.exit()
        except requests.ConnectionError:
            print('Please Turn On NetWork Connection!')
            sys.exit() 
    
