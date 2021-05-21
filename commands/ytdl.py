from __future__ import unicode_literals
import youtube_dl

def ytdl_get(url, info):
    info = info.strip()

    ytdl_opts = {}
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        video_info = ytdl.extract_info(url, download=False)
        return str(video_info[info])
