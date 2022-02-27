

from pprint import pprint
import disnake

from disnake.ext import commands,tasks
import re


from. import exceptions


import os



class MusicCmd(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        self.songRepeat=False
        self.queueLoop=False

        self._playlist=[]
        self.currentSong=None

    def _in_vc_check(self, ctx):
        if ctx.author.voice is None:
            raise commands.CommandError(
                "U to need join a voice channel first!")

    async def _log(self, ctx, msg):
        await ctx.send(msg)

    @commands.command("error")
    async def cmdtest_error(self, ctx):
        raise commands.CommandError("U noob")

    @commands.command(name="join")
    async def cmd_join(self, ctx):
        self._in_vc_check(ctx)
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        return await ctx.voice_client.move_to(ctx.author.voice.channel)


    @commands.command(name="leave")
    async def cmd_leave(self, ctx):
        self._in_vc_check(ctx)
        await ctx.voice_client.disconnect()

    @commands.command(name="pause")
    async def cmd_pause(self, ctx):
        self._in_vc_check(ctx)
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()

    # TODO volume control
    @commands.command(name="volume")
    async def cmd_volume(self, ctx, vol: int):
        pass


    def _play(self,ctx,ytURL):
        ytCode = ytURL.replace("?", "/").split("/")[-1]

        #TODO YTDL 控制

        filename = f"audioCache\\{ytCode}.mp3"
        if os.path.exists(filename):
            source = disnake.PCMVolumeTransformer(disnake.FFmpegPCMAudio(filename), volume=0.1)
            ctx.voice_client.play(source, after=self._playing_end)

    def _playing_end(self,error=None):
        if self.songRepeat:
            self._playlist.insert(0,self.currentSong)
        elif self.queueLoop:
            self._playlist.append(self.currentSong)

    @commands.command(name="play")
    async def cmd_play(self, ctx, *, url: str or None = None):
        self._in_vc_check(ctx)
        if ctx.voice_client is None:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
        elif url is None:
            if ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                return
            else:
                raise commands.BadArgument(
                    "Is ur URL link has been eaten by Paimon?")
        ytUrl = re.match(
            "http[s]?:\/\/(www.youtube.com\/watch\?v=|youtu.be\/)[\w-_\d]{11}", url).group()
        self._play(ctx,ytUrl)



