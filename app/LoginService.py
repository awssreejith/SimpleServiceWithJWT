from flask import Flask
from flask import request ##This is a good addon for authentication
from flask import jsonify
import jwt
import datetime
import functools

##Our local B of users and passwords

userDB = [{"user" : "Isser_Harel",    "password" : "mossad_1"},
          {"user" : "Meir_Amit",      "password" : "mossad_2"},
          {"user" : "Ruven_Shiloah",  "password" : "mossad_3"}
         ]
         
emptyPasswdError     = 0
userDoesntExistError = 1
emptyToken           = 2
invalidToken         = 3
wrongPasswdError     = 4
loginSuccess         = 5
tokenSuccess         = 6
         
errorDB = [
            {"Status" : "Failed", "Message" : "LoginID/Password can't be empty","Code":103},
            {"Status" : "Failed", "Message" : "User doesn't exist","Code":107},
            {"Status" : "Failed", "Message" : "Empty Token provided","Code":109},
            {"Status" : "Failed", "Message" : "Invalid Token provided","Code":111},
            {"Status" : "Failed", "Message" : "Wrong password for the user provided","Code":113},
            {"Status" : "Success","Message" : "Login Succesful","Code":117},
            {"Status" : "Success","Message" : "Token validated succesfully","Code":123}
          ]

App = Flask("LOGIN SERVICE")
##For the time being, we just use application wide secret key
App.config['SECRET_KEY'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def processInputRequestDecorator(func):
    ##The usage of this decorator is to check whether the incoming request
    ##has the JWT. Ifo not we simply return missing JWT error. Else we decode and JWT and check whether
    ##the secret key is similar to App.config['SECRET_KEY'] value
    @functools.wraps(func)
    def extractJWT(*args, **kwargs):
        ##When a user sends the request, he sends as below
        ## curl -X GET http://127.0.0.1:5000/data?MyToken=blahblahblah
        ## We extract only the field MyToken=blahblahblah and decode the blahblahblah and verify
        ## whether the decoded string equals App.config['SECRET_KEY'] value
        payLoadTokenString = request.args.get('MyToken')
        if payLoadTokenString == None or len(payLoadTokenString) <= 0 or payLoadTokenString == '':
            return errorDB[emptyToken]
        return (func(request,payLoadTokenString))

    return extractJWT

@App.route('/login',methods=['POST'])
def doLogin():
    LS = LoginService()
    ret = LS.processLogin(request)
    return jsonify(ret)

##The following route is used if the user is authenticated and uses the valid JWT with the request
@App.route('/data',methods=['get'])
@processInputRequestDecorator
def processInputRequest(*args, **kwargs):
    request = args[0] ##anyway not used
    token   = args[1]

    lService = LoginService()
    return(jsonify(lService.validateToken(token)))


    
class LoginService(object):
    def __init__(self):
        pass
        
    def processLogin(self,request):
        
        user   = request.authorization['username']
        passwd = request.authorization['password']
        
        if user == '' or passwd == '':
            return errorDB[emptyPasswdError]

        ret,errorJSON = self.validateUserPassword(user,passwd)
        if ret == False:
            return errorJSON   
 
        ## login succesful. Now create JWT token.
        ## Here we create two types of token - token with simply username and tokn with user name and expiration
        ##We pass his password also so that it will be his secret key
        ## token = self.createJWTtoken(user,usernameToken = True,expiration = False)
        token = self.createJWTtoken(user,usernameToken = True,expiration = True)  ##Create a token which expires in 1 minute
        ##VERY IMPORTANT
        ##The token returned will be in byte format and JSON is not byte serializable.
        ## So we have to convert it to string as below.
        tokenToString = token.decode('UTF-8')
        retPayload = errorDB[loginSuccess]
        retPayload["key"] = tokenToString
        ##The entire steps can be wrapped under a single step as below
        ##############################################################
        ## errorDB[loginSuccess]["key"] = self.createJWTtoken(user,passwd,usernameToken = True,expiration = False).decode('UTF-8')
        ## return errorDB[loginSuccess]
        ##############################################################
        return retPayload
     

    def createJWTtoken(self,user,usernameToken=True,expiration = False): # by default we create only with user name payload
        payLoad = {}
        if usernameToken == True:
            payLoad['user'] = user
            ##Add some more payload data
            payLoad['branch'] = 'Mossad'
            payLoad['region'] = 'Tel Aviv'
            payLoad['Prime Minister'] = 'David Ben Gurion'
            
        if expiration == True:
        ## just set expiration after 30 minutes
            timeToExpire = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
            payLoad['exp'] = timeToExpire
            
        encoded = jwt.encode(payLoad,key=App.config['SECRET_KEY'])
        return encoded

    def validateUserPassword(self,user,passwd):
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
            return False,errorDB[userDoesntExistError]
            
        if passwdForUser != passwd:
            return False,errorDB[wrongPasswdError]

        return True,None

    def validateToken(self,token):
        decode = {}
        try:
           decode = jwt.decode(token,App.config['SECRET_KEY'])
        except BaseException as B:
            print("Invalid Token"+"\n")
            return errorDB[invalidToken]

        print(decode)
        return errorDB[tokenSuccess]

    
    def run(self):
            App.run(debug=True)
            
        
        
    