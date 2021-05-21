message = text.split(":")
MESSAGE_INDEX = 2
COMMAND_INDEX = 1

def get_message(message):
    #!mpvbot [command] (args...)
    if message[MESSAGE_INDEX].startswith("!mpvbot"):
        cmd_message = []
        cmd = message[MESSAGE_INDEX].split(" ")

        for n in range(1, len(cmd)):
            cmd_message.append(cmd[n])

        return get_command(cmd_message)
    else:
        return None

def get_command(command):
    command = str(command[COMMAND_INDEX]).strip()

    cmd_bind = command_aliases[command]

    return set_command(cmd_bind, command)

def set_command(binding, args):
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

    return run_command(cmd_call, args)

def run_command(cmd_call, args):
    cmd = str(args[CMD_INDEX])

    if (cmd == "ping"):
        return cmd_call.ping()
    if (cmd == "help"):
        return cmd_call.help()
    if (cmd == "ytdl"):
        return cmd_call.ytdl_title(args[1])
    if (cmd == "chan"):
        return cmd_call.ytdl_channel(args[1])
    if (cmd == "info"):
        return cmd_call.ytdl_get(args[1], args[2])
    if (cmd == "rss"):
        return cmd_call.language()
    if (cmd == "atom"):
        return cmd_call.getFeedTitle()

    return "Command not found."
