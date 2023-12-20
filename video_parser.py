from __future__ import unicode_literals
# import youtube_dl
import yt_dlp as youtube_dl
import os
from collections import deque

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'outtmpl' : '',
}
# lien = "https://www.youtube.com/watch?v=OZ9hY4SNBvk"
# youtu = youtube_dl.YoutubeDL(ydl_opts)
# # testons= youtu.extract_info(lien, download=False
# cherche = 'food wars snow drop'
# testons= youtu.extract_info(f'ytsearch:{cherche}', download=False)
# # print(testons)
# x = youtu.prepare_filename(testons)

# for elem in testons['entries'][:5]:
#     print(elem['title'])

# # y = youtu.download(lien)

# print('fini')

# print('infos nom : ', testons['title'])
# duree = testons['duration']
# print('infos duree : ', str(int(duree) // 60) + ':' + str(int(duree) % 60))
# print(youtu.report_file_already_downloaded(lien))

# print(x)
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     ydl.download(['https://www.youtube.com/watch?v=ujTCoH21GlA&list=PLzMcBGfZo4-mP7qA9cagf68V06sko5otr'])

class Music_player():
    def __init__(self) :        
        #the index of the last song sent to the flow
        self.last_element = 0
        
        # we are going to use a list because we need the order, reminder : if it gets to big use queue datastructure
        self.queue = deque([])
        self.name_actual = ''

        # if clear == True :
        self.clear_queue()

    #set up the queue with the song from last session
    def clear_queue(self):
        for file in os.listdir('zik'):
            os.remove('zik/' + file)

        self.queue = deque([])

    def update_file_name(self):
        index = len(self.queue)
        ydl_opts['outtmpl'] = 'zik/son' + str(index)
        self.name_actual = 'son'+str(index)

    def add_dl(self, lien):
        self.update_file_name()
        player = youtube_dl.YoutubeDL(ydl_opts)
        all_infos = player.extract_info(lien, download=True )

        nom = all_infos['title']
        duree = all_infos['duration']
        lien = 'zik/'+ self.name_actual + '.mp3'
        
        data_song = {'nom':nom , 'duree':duree , 'lien':lien }
        
        self.queue.appendleft(data_song)

        return data_song

    def get_song(self):
        while len(self.queue) > 0 :
            song = self.queue.pop()

            yield song

        else :
            return False


    def play_song_fast(self, lien):
        ydl_opts['outtmpl'] = 'zik/son'
        player = youtube_dl.YoutubeDL(ydl_opts)

        info = player.extract_info(lien, download=True)

        data = {'nom':info['title'] , 'duree':info['duration']}

        return data
    

# test = Music_player()

# lien1 = 'https://www.youtube.com/watch?v=aCIsEOp8CS0'

# lien2 = 'https://www.youtube.com/watch?v=L1FdEBTJXus'

# lien3 = 'https://www.youtube.com/watch?v=YRU7MZWDmgg'

# all_liens = [lien1, lien2, lien3]

# for li in all_liens :
#     not_found = True
#     test.add_dl(li)


#     song = next(test.get_song()) 

#     print(song['nom'])

