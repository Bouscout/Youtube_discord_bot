import discord 
from discord import app_commands, FFmpegPCMAudio
from discord.ext import commands


TOKEN = 'MTA4NjA4Nzk0NTk3MjM3MTU1OA.GKE-_0.Xm_kDw10QKjdX0k68gL4FVFe6Eb0xAgsHyhij8'
CHANEL_ID = 1086089280868319276
VOICE_CHANNEL = 1086089280868319277

GUILD_ID = 1086089280868319272



class the_bot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.all())

    async def on_ready(self):
        chanel = self.get_channel(CHANEL_ID)
        fmt = await tree.sync(guild=discord.Object(id=str(GUILD_ID)))
        await chanel.send(f'je suis la les gars  {len(fmt)}')

bot = the_bot()
tree = app_commands.CommandTree(bot)

@tree.command(name='ping')
async def ping(ctx : discord.Interaction):
    await ctx.send('pong !!')

bot.run(TOKEN)