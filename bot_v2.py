import discord
from discord.ext import commands
from discord import app_commands, FFmpegPCMAudio
import sys, asyncio
from link_parse import Link_parser
from video_parser import Music_player
from collections import deque
from flow import flow_zik
import os
from dotenv import load_dotenv

load_dotenv()


FLOW = flow_zik()

# server and bot informations
TOKEN = os.getenv("TOKEN")
CHANEL_ID = os.getenv("CHANEL_ID")
GUILD_ID = os.getenv("GUILD_ID")

# state controller
PLAYING = False
IN_VC = False


Guild = discord.Object(id=str(GUILD_ID))

intentions = discord.Intents.all()
intentions.members = True

player = Music_player()


bot = commands.Bot(command_prefix='/', intents=intentions)

# when he first join the chanel
@bot.event
async def on_ready():
    chanel = bot.get_channel(CHANEL_ID)
    await chanel.send('...')

#in order to sync the commands to the tree
@bot.command(name='sync')
async def sync(ctx):
    bot.tree.copy_global_to(guild=Guild)
    fmt = await bot.tree.sync(guild=Guild)
    await ctx.send(f'{len(fmt)} commands were synced')

#to plpay the songs in a certain playlist
@bot.tree.command(name='playlist', description='''Bot va jouer les son a dans la playlist''')
async def playlist(ctx : discord.Interaction, *, nom_playlist: str = 'default'):
    global IN_VC
    if nom_playlist + '.csv' in os.listdir('playlist') :
        fichier_name = 'playlist/' + nom_playlist + '.csv'
        asyncio.create_task(FLOW.handle_playlist(fichier_name))

        # join the voice chanel
        if discord.utils.get(bot.voice_clients, guild=ctx.guild):
            IN_VC = True

        else :
            IN_VC = False
            guild = ctx.guild
            vc = guild.voice_channels[0]
            await vc.connect()
            IN_VC = True
            # await FLOW.handle_playlist(fichier_name)
            await asyncio.sleep(5)
            await FLOW.music_queue_player(ctx=ctx, vc=ctx.guild.voice_client)

    else :
        page = discord.Embed(
        title='Playlist',
        description=f'playlist non trouvée : {nom_playlist}',
        colour =  discord.Colour.blue()
        )
        page.set_footer(text='👌')

        await ctx.response.send_message(embed=page)



@bot.tree.command(name='add_playlist', description='''Bot va ajouter des songs a la playlist fournies''')
async def add_playlist(ctx : discord.Interaction, *, nom_playlist: str = 'default'):
    if nom_playlist.lower() == 'stop' :
        page = discord.Embed(
        title='Playlist',
        description=f'je ferme la playlist {FLOW.add_playlist}',
        colour =  discord.Colour.blue()
        )
        page.set_footer(text='👌')

        FLOW.add_playlist = False
        FLOW.song_in_playlist = []
    else :
        FLOW.add_playlist = nom_playlist
        page = discord.Embed(
        title='Playlist',
        description=f'ajoutons des sons a la playlist {nom_playlist}',
        colour =  discord.Colour.blue()
        )
        page.set_footer(text='👌')
        FLOW.song_in_playlist = []
       
        
    await ctx.response.send_message(embed=page)

#to check if the bot is present pong
@bot.tree.command(name='ping', description='Bot will say pong back')
async def ping(ctx : discord.Interaction):
    print('on a au moins recu le message')
    print('the guild id : ', ctx.guild_id)
    page = discord.Embed(
        title='Test',
        description='Je suis suppose dire pong la, merde',
        colour =  discord.Colour.blue()
    )
    page.set_footer(text='Amuse toi ')
    page.add_field(
        name='Prefix',
        value='The current prefix is /',
        inline=True,
    )
    
    await ctx.response.send_message(embed=page)




#command for the bot to play some music
@bot.tree.command(name='play', description='The bot will play the music you want 👌')
@app_commands.describe()
async def play(ctx : discord.Interaction, *, nom : str ):
    global IN_VC, PLAYING
    serch = ''
   
    for x in nom :
        serch += x

    serch_words = serch.split(' ')
    
    
    print('the test is : ', serch)

    # check if the bot is already playing a song to not skip it
    if discord.utils.get(bot.voice_clients, guild=ctx.guild) and ctx.guild.voice_client.is_playing():

       
        # chanel = bot.get_channel(CHANEL_ID)
        # await chanel.send('Ajouter a la queue: '+serch)
        await ctx.response.send_message('Ajoutez a la file d\'attente : '+ serch )
        
        
        infos = FLOW.handle_request(serch_words)

        print('nouvelles infos : ', infos)

        FLOW.tail.appendleft(infos)

        # download and prepare the song to be played

        # add it to the queue
        print('jusque la')
        if FLOW.playing == False:
            print('il joue deja')
            FLOW.playing = True
            await FLOW.music_queue_player(ctx=ctx, vc=ctx.guild.voice_client)
        return


    # if the bot is not in the voice channel
    await ctx.response.send_message('Vous avez demandez : ' + serch)

    # let's clear the queue of all the old songs then play the request
    FLOW.player.clear_queue()
    infos = FLOW.handle_single(serch_words)
    
    # check if the bot is in the voice chanel and then connect it
    if discord.utils.get(bot.voice_clients, guild=ctx.guild):
        IN_VC = True
        pass
    else :
        IN_VC = False
        guild = ctx.guild
        vc = guild.voice_channels[0]
        await vc.connect()
        IN_VC = True

    try :
        zik = FFmpegPCMAudio('zik/son.mp3')
        ctx.guild.voice_client.play(zik)

        await FLOW.song_info(ctx=ctx, info=infos)

    except PermissionError :
        print('erreur attrape')


 

@bot.tree.command(name='skip', description='The bot will skip the current song')
async def skip(ctx : discord.Interaction):
    vc = ctx.guild.voice_client
    if vc.is_playing():
        vc.stop()
        FLOW.skip = True
        
    await ctx.response.send_message('Skipped')
    return

@bot.tree.command(name='repeat', description='Make the bot repeat or stop repeat of the actual song ')
async def repeat(ctx : discord.Interaction):
    print('tente te repeter')
    vc = ctx.guild.voice_client
    if vc.is_playing():
        FLOW.repeat = not FLOW.repeat
        print('ca va se repeter') 
        # await FLOW.song_info(ctx=ctx)



#general command : make the bot join the voice chanel
@bot.command()
async def join(ctx):
    if ctx.message.author.voice :
        channel = ctx.message.author.voice.channel
    else : channel = None

    if channel : await channel.connect()
    else : await ctx.send('bah rejoins le salon d\'abord 😑')

#general command : ask the bot to leave if he is in a voice chanel
@bot.command()
async def leave(ctx):
    print('on fait juste un test : ', ctx.voice_client)
    voix = ctx.voice_client
    if voix : await voix.disconnect()
    else : ctx.send('bruhhh je suis meme pas dans le salon 😂')

@bot.command()
async def close(ctx):
    await ctx.send('Je decale 🙌')
    #do all the data collecting you need

    sys.exit()


bot.run(TOKEN)

input('appuyez entrez pour fermer le programme')