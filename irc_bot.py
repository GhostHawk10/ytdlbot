from irc_class import *
from irc_config import *
from commands.atom import *
import os
import random
import logging
from threading import *

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "logs/log.txt", level = logging.DEBUG, format = LOG_FORMAT)
logger = logging.getLogger()

logger.info("Initialize bot.")

logger.info("Load config.")
user = loadconfig("config/global")
connection = { "server":user["server"], "port":int(user["port"]) }
logger.info("Load user.")

logger.info("Set command aliases.")
command_aliases = {
    "info":"ytdl",
    "atom":"atom",
}

logger.info("Connect to IRC network.")
irc = IRC()
irc.connect(connection, user)

MESSAGE_INDEX = 2
COMMAND_INDEX = 1

class BroadcastThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(int(update_interval)):
            broadcast_message = broadcast_ready()
            if broadcast_message != "":
                irc.send(user, broadcast_message)

    def begin_timer():
        stopFlag = Event()
        thread = BroadcastThread(stopFlag)
        thread.start()
        #stopFlag.set()

def get_message(message):
    #!ytdlbot [command] (args...)
    message = text.split(":", 2)
    
    logger.info("Format raw IRC message into parsed message.")
    full_message = message[MESSAGE_INDEX]

    if full_message.startswith("!" + user["username"]):
        cmd_message = []
        cmd = full_message.split(" ")
        
        for n in range(0, len(cmd)):
            cmd_message.append(cmd[n])

        return get_command(cmd_message)
    else:
        return None

def get_command(command):
    cmd = str(command[COMMAND_INDEX]).strip()
    args = get_args(command)

    try:
        cmd_bind = command_aliases[cmd]
    except KeyError as e:
        print(e)
        return "Command not found."

    return set_command(cmd_bind, cmd, args)

def get_args(command):
    args = []
    for a in range(2, len(command)):
        args.append(command[a].strip())

    return args

def set_command(binding, cmd, args):
    try:
        mod = "commands." + binding
        mod = __import__(mod, globals(), locals(), [])
    except ImportError as e:
        print(e)
        return None

    try:
        cmd_call = getattr(mod, binding)
    except AttributeError as e:
        print(e)
        return None

    return run_command(cmd_call, cmd, args)

def run_command(cmd_call, cmd, args):
    logger.info("Attempt execute command: " + cmd)

    if (cmd == "info"):
        return cmd_call.ytdl_get(args[0], args[1])
    if (cmd == "atom"):
        BroadcastThread.begin_timer()
        return "Toggled broadcasting."

    return cmd

def get_nick(message):
    identity = message.split(":")
    nick = identity[1].split(" ")
    
    return nick[0].split("!")[0]

while True:
    text = irc.get_response()
    print(text)

    message = text.split(" ")

    if "PRIVMSG" in text and user["channel"] in text:
        to_send = get_message(message)
        if len(message) >= 3 and to_send != None:
            irc.send_notice(get_nick(text), to_send)
