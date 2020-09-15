import discord
from discord.ext import commands
import requests
from module import language, usagetime


# language load
class_load = language
language_json = class_load.load_language_english()

url = 'https://status.mojang.com/check'
response = requests.get(url)
jsonData = response.json()

# Mojang API Status
# minecraft.net
if jsonData[0]["minecraft.net"] == "red":
    mn = "\N{LARGE RED CIRCLE}"
elif jsonData[0]["minecraft.net"] == "yellow":
    mn = "\N{LARGE YELLOW CIRCLE}"
elif jsonData[0]["minecraft.net"] == "green":
    mn = "\N{LARGE GREEN CIRCLE}"

# session.minecraft.net
if jsonData[1]["session.minecraft.net"] == "red":
    smn = "\N{LARGE RED CIRCLE}"
elif jsonData[1]["session.minecraft.net"] == "yellow":
    smn = "\N{LARGE YELLOW CIRCLE}"
elif jsonData[1]["session.minecraft.net"] == "green":
    smn = "\N{LARGE GREEN CIRCLE}"

# account.mojang.com
if jsonData[2]["account.mojang.com"] == "red":
    accmc = "\N{LARGE RED CIRCLE}"
elif jsonData[2]["account.mojang.com"] == "yellow":
    accmc = "\N{LARGE YELLOW CIRCLE}"
elif jsonData[2]["account.mojang.com"] == "green":
    accmc = "\N{LARGE GREEN CIRCLE}"

# authserver.mojang.com
if jsonData[3]["authserver.mojang.com"] == "red":
    authservermc = "\N{LARGE RED CIRCLE}"
elif jsonData[3]["authserver.mojang.com"] == "yellow":
    authservermc = "\N{LARGE YELLOW CIRCLE}"
elif jsonData[3]["authserver.mojang.com"] == "green":
    authservermc = "\N{LARGE GREEN CIRCLE}"

# sessionserver.mojang.com
if jsonData[4]["sessionserver.mojang.com"] == "red":
    ssmc = "\N{LARGE RED CIRCLE}"
elif jsonData[4]["sessionserver.mojang.com"] == "yellow":
    ssmc = "\N{LARGE YELLOW CIRCLE}"
elif jsonData[4]["sessionserver.mojang.com"] == "green":
    ssmc = "\N{LARGE GREEN CIRCLE}"

# api.mojang.com
if jsonData[5]["api.mojang.com"] == "red":
    apimc = "\N{LARGE RED CIRCLE}"
elif jsonData[5]["api.mojang.com"] == "yellow":
    apimc = "\N{LARGE YELLOW CIRCLE}"
elif jsonData[5]["api.mojang.com"] == "green":
    apimc = "\N{LARGE GREEN CIRCLE}"

# textures.minecraft.net
if jsonData[6]["textures.minecraft.net"] == "red":
    texturesmc = "\N{LARGE RED CIRCLE}"
elif jsonData[6]["textures.minecraft.net"] == "yellow":
    texturesmc = "\N{LARGE YELLOW CIRCLE}"
elif jsonData[6]["textures.minecraft.net"] == "green":
    texturesmc = "\N{LARGE GREEN CIRCLE}"

# mojang.com
if jsonData[7]["mojang.com"] == "red":
    mojangcom = "\N{LARGE RED CIRCLE}"
elif jsonData[7]["mojang.com"] == "yellow":
    mojangcom = "\N{LARGE YELLOW CIRCLE}"
elif jsonData[7]["mojang.com"] == "green":
    mojangcom = "\N{LARGE GREEN CIRCLE}"


class status_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='status', invoke_without_command=True)
    async def statuscommand(self, ctx):
        usagetime.write_usagetime("status")

        embed = discord.Embed(title="Mojang API Status", description=f"\N{LARGE GREEN CIRCLE} (no issues)\n"
                                                                     f"\N{LARGE YELLOW CIRCLE} (some issues)\n"
                                                                     f"\N{LARGE RED CIRCLE} (service unavailable)\n")
        embed.add_field(name="minecraft.net", value=f"[ {mn} ]", inline=False)
        embed.add_field(name="session.minecraft.net", value=f"[ {smn} ]", inline=False)
        embed.add_field(name="account.mojang.com", value=f"[ {accmc} ]", inline=False)
        embed.add_field(name="authserver.mojang.com", value=f"[ {authservermc} ]", inline=False)
        embed.add_field(name="sessionserver.mojang.com", value=f"[ {ssmc} ]", inline=False)
        embed.add_field(name="api.mojang.com", value=f"[ {apimc} ]", inline=False)
        embed.add_field(name="textures.minecraft.net", value=f"[ {texturesmc} ]", inline=False)
        embed.add_field(name="mojang.com", value=f"[ {mojangcom} ]", inline=False)
        embed.set_footer(text=f"{language_json['english']['embed_footer_message']}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(status_cog(bot))
