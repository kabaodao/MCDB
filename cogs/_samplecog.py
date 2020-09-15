import discord
from discord.ext import commands

class samplecog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='sample', invoke_without_command=True)
    async def samplecommand(self, ctx):
        await ctx.send('sample')

    @samplecommand.command(name='abc')
    async def abc_samplecommand(self, ctx):
        await ctx.send('abc')

def setup(bot):
    bot.add_cog(samplecog(bot))