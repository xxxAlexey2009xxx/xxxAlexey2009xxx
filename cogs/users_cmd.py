import disnake
from disnake.ext import commands
from random import randint


class CMDUsers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} is ready to work!")
        await self.bot.change_presence(activity=disnake.Game("Dota 2"))

    @commands.slash_command(description='время нужное для набора рейтинга, по дефолту 86400'):
def setup(bot):
    bot.add_cog(CMDUsers(bot))
