from flask import Flask
from flask import request
from flask import jsonify

##Our local B of users and passwords

userDB = [{"user" : "Isser_Harel",    "password" : "mossad_1"},
          {"user" : "Meir_Amit",      "password" : "mossad_2"},
          {"user" : "Ruven_Shiloah",  "password" : "mossad_3"}
         ]
         
emptyPasswdError     = 0
userDoesntExistError = 1
wrongPasswdError     = 2
loginSuccess         = 3
         
errorDB = [
            {"Status" : "Failed", "Message" : "LoginID/Password can't be empty","Code":103},
            {"Status" : "Failed", "Message" : "User doesn't exist","Code":107},
            {"Status" : "Failed", "Message" : "Wrong password for the user provided","Code":109},
            {"Status" : "Success","Message" : "Login Succesful","Code":111}
          ]

App = Flask("LOGIN SERVICE")

@App.route('/login',methods=['POST'])
def doLogin():
    LS = LoginService()
    ret = LS.processLogin(request)
    return jsonify(ret)
    
class LoginService(object):
    def __init__(self):
        pass
        
    def processLogin(self,request):
        
        user   = request.authorization['username']
        passwd = request.authorization['password']
        
        if user == '' or passwd == '':
            return errorDB[emptyPasswdError]
        
        ##check only for regitered user
        userExist = False
        passwdForUser = ''
        for element in userDB:
            for key in element:
                if key == 'user':
                    if element[key] == user:
                        passwdForUser = element['password']
                        userExist = True
                        break
                        
            if userExist == True:
                break
                
        if userExist == False:
            return errorDB[userDoesntExistError]
            
        if passwdForUser != passwd:
            return errorDB[wrongPasswdError]
            
        return errorDB[loginSuccess]
            
    
    def run(self):
            App.run(debug=True)
            
        
        
    