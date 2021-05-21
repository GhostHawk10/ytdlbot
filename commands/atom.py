from irc_config import *
import feedparser

feed_dict = loadconfig("config/feeds")
f = feedparser.parse(feed_dict["feed"])

update_interval = feed_dict["update-interval"]
last_broadcast = ""
cur_broadcast = ""
LATEST = 0

def get_broadcast_message():
    f = feedparser.parse(feed_dict["feed"])
    return str.format("Latest from {0} - {1} - {2}", f.feed.title, f.entries[LATEST].title, f.entries[LATEST].link)

def broadcast(): 
    return cur_broadcast

def broadcast_ready():
    global last_broadcast
    global cur_broadcast   
    cur_broadcast = get_broadcast_message()
    
    if is_repeat_broadcast():
        return ""
    else:
        last_broadcast = cur_broadcast
        return broadcast()

    return "failed"

def is_repeat_broadcast():
    global last_broadcast
    global cur_broadcast
    return (last_broadcast == cur_broadcast)



