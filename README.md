Here we accept a simple user-ID and password and authenticate with the user id and password stored in a JSON.
If it matches, then we return login succesful JSON message. Else error JSON message

In the second phase We use JWT for autherization for each request

To send usrid and password for the first time
        curl -u Isser_Harel:mossad_1 -X POST http://127.0.0.1:5000/login
                <userid>   <password>

To send request with token which we got from above
        curl  -X GET  http://127.0.0.1:5000/data?MyToken=173hdumr94d=sjedmwkwowsmk8756hskd09juy8dt647g97
                                                         <TOKEN WE GOT AFTER RUNNING THE FIRST COMMAND>





*********************  REQUIREMENTS  ****************************************

0)jwt

sudo pip3 install PyJWT

1) datetime

sudo pip3 install datetime

