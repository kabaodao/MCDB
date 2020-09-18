import discord
from discord.ext import commands
from module import usagetime


class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="help", invoke_without_command=True)
    async def helpcommand(self, ctx):
        usagetime.write_usagetime("help")

        embed = discord.Embed(title="MCDB's Help Page", description="Thank you for Using MCDB!")
        embed.add_field(name="Prefix", value="`m.` **__This Prefix is required at the beginning.__**", inline=False)
        embed.add_field(name="Argument", value="`<argument>` - **__This argument is a required.__**", inline=False)
        embed.add_field(name="Help", value="`help` - Show this page.\n", inline=False)
        embed.add_field(name="History", value="`history <MCID/UUID>` - Show the player's name history.", inline=False)
        embed.add_field(name="Profile", value="`profile <MCID/UUID>` - Show the player's name profile", inline=False)
        embed.add_field(name="API Status", value="`status` - Show the mojang API status.")
        embed.add_field(name="Information", value="[mojang.com](https://www.mojang.com/)\n"
                                                  "[api.mojang.com](https://api.mojang.com/)\n"
                                                  "[minecraft.net](https://www.minecraft.net/)\n"
                                                  "[minotar.net](https://minotar.net/) - Copyright 2018 axxim.net", inline=False)
        embed.add_field(name="Developed by", value="[@KabaoDao](https://twitter.com/KabaoDao)")
        embed.add_field(name="FeedBack", value="Pls send to `KabaoDao#7271`")
        embed.add_field(name="Invite URL", value="[Click Here](https://discord.com/oauth2/authorize?client_id=748910923091279914&permissions=26688&scope=bot)")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.group(name="bot", invoke_without_command=True)
    async def botcommand(self, ctx):
        await ctx.send("usagetime / s3")

    @commands.is_owner()
    @botcommand.command(name="usagetime")
    async def usagetime_botcommand(self, ctx):
        usagetime_obj = usagetime.load_usagetime()
        total = usagetime_obj['help'] + usagetime_obj['history'] + usagetime_obj['profile'] + usagetime_obj['status']
        await ctx.send(f"help - {usagetime_obj['help']}\n"
                       f"history - {usagetime_obj['history']}\n"
                       f"profile - {usagetime_obj['profile']}\n"
                       f"status - {usagetime_obj['status']}\n"
                       f"total - {total}")

    @commands.is_owner()
    @botcommand.command(name="s3")
    async def s3_botcommand(self, ctx):
        usagetime.upload_usagetime()
        await ctx.send("Done")


def setup(bot):
    bot.add_cog(help_cog(bot))
