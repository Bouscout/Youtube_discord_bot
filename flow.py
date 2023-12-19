from collections import deque
import csv

from video_parser import Music_player
from link_parse import Link_parser
from asyncio import sleep
from discord import FFmpegPCMAudio
import discord

class flow_zik(Link_parser):
    def __init__(self) :
        super().__init__()
        self.tail = deque([])
        self.player = Music_player()
        self.playing = False

        self.actual_song = None
        
        #in order to control the skipping of songs
        self.skip = False

        #in order to control if son if played on repeat
        self.repeat = False

        #in order to keep adding this song to a plalist
        self.add_playlist = False
        self.song_in_playlist = []
    
    #function to handle all the incoming request through a multiprocessing pipe
    def handle_request(self, mot):

        #processing the words into usable link and then search it on google
        print('le mot est : ', mot)

        self.process_words(words=mot)
        liens = self.analyze_link()
        google_link = liens[0]

        #passe the good link and download it before returning the info dict
        infos = self.player.add_dl(liens[0])

        # checkig if we need to add to the playlist
        if self.add_playlist :
            self.add_to_playlist(lien=google_link, infos=infos)

        #send back the info to the main process
        return infos
    
    # to handle a request for only one song in case first song played
    def handle_single(self, words):
        # process the words into usable google links
        self.process_words(words=words)
        liens = self.analyze_link()

        google_link = liens[0]
        #download and pass the info of the song
        infos = self.player.play_song_fast(liens[0])

        # checking if we need to add to the playlist
        if self.add_playlist :
            self.add_to_playlist(lien=google_link, infos=infos)

        return infos
    
    # function to handle the process of checking if the music is over then playing next
    async def music_queue_player(self, ctx, vc):
        print('on teste la porte')

        while len(self.tail) > 0 or self.repeat == True :
            if ctx.guild.voice_client.is_playing() and self.skip == False:
                await sleep(5)
                continue

            # resseting the skip value for next iteration
            self.skip = False
            
            if self.repeat == False :
                infos = self.tail.pop()
                print('popped new value')

            son = FFmpegPCMAudio(infos['lien'])
            vc.play(son)

            self.actual_song = infos

            # to display the song infos on the discord chat
            await self.song_info(ctx=ctx, info=infos)

            print('music jouer : ', infos['nom'])

            self.repeat = False

        print('plus rien ')
        self.playing = False


    # function to send the song infos to the discord server
    async def song_info(self, ctx, info=None):

        # get the actual song info from either the request or the queue
        infos = self.actual_song if not info else info 

        # wrapping it in the discord embed
        nom, duree = infos['nom'], infos['duree']

        duree = str(duree // 60) + ' : ' + str(duree % 60)
  
        page = discord.Embed(
            title='Music',
            description=nom,
            colour =  discord.Colour.blue()
        )
        page.set_footer(text='👌')
        page.add_field(
            name='Duration',
            value=duree,
            inline=True,
        )

        await ctx.channel.send(embed=page)

        #send them through a discord message

    # function to add song to a certain playlist
    def add_to_playlist(self, lien: str, infos: dict):

        # checking if the song is already in the playlist
        if len(self.song_in_playlist) == 0 :
            try :
                with open(f'playlist/{self.add_playlist}.csv', 'r', encoding='utf-8') as fichier :
                    reader = csv.reader(fichier)
                    for line in reader :
                        nom, lien = line
                        self.song_in_playlist.append(nom)
            except :
                pass

        if infos['nom'] in self.song_in_playlist :
            return # no need to add it to the playlist


        fields = ['nom', 'lien']
        info_dict = {'nom':infos['nom'], 'lien':lien}
        with open(f'playlist/{self.add_playlist}.csv', 'a', encoding='utf-8') as fichier :
            writer = csv.DictWriter(fichier, fieldnames=fields, dialect='excel')
            writer.writerow(info_dict)

        self.song_in_playlist.append(info_dict['nom'])
        
            
    # in order to play the songs in a certain playlist
    async def handle_playlist(self, fichier):
        with open(fichier, 'r', encoding='utf-8') as f :
            reader = csv.reader(f)
            for line in reader :
                if len(line) > 0 :
                    nom, lien = line
                    info = self.handle_request(lien)
                    self.tail.appendleft(info)

        self.playing = True
        return