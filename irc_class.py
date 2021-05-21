import socket
import sys
import time

class IRC:
    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, user, msg):
        self.irc.send(bytes(str.encode("PRIVMSG " + user["channel"] + " " + ":" + msg + "\n")))

    def send_notice(self, target, msg):
        self.irc.send(bytes(str.encode("NOTICE " + target + " " + ":" + msg + "\n")))

    def connect(self, connection, user):
        print("Connecting to: " + connection["server"])
        self.irc.connect((connection["server"], connection["port"]))

        self.authenticate(user)
        self.join(user)

    def authenticate(self, user):
        self.irc.send(bytes(str.encode("USER " + self.set_user(user) + " :python\n")))
        self.irc.send(bytes(str.encode("NICK " + user["username"] + "\n")))
        #self.irc.send(bytes("NICKSERV IDENTIFY " + botnickpass + " " + botpass + "\n").encode("UTF-8"))
        time.sleep(5)

    def set_user(self, user):
        return str.format("{0} {1} {2} {3}", user["username"], user["hostname"], user["servername"], user["realname"])

    def join(self, user):
        self.irc.send(bytes(str.encode("JOIN " + user["channel"] + "\n")))
        
    def get_response(self):
        time.sleep(1)
        resp = self.irc.recv(2040).decode("UTF-8")
 
        if resp.find('PING') != -1:                      
            self.irc.send(bytes(str.encode('PONG ' + resp.split() [1] + '\r\n'))) 
 
        return resp
