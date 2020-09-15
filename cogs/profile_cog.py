import discord
from discord.ext import commands
from datetime import datetime
from module import mojang_api_url, language, usagetime


# language load
class_load = language
language_json = class_load.load_language_english()


class profile_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='profile', invoke_without_command=True)
    async def profilecommand(self, ctx, mciduuid):
        usagetime.write_usagetime("profile")

        # argument(mciduuid) to UUID
        mojang_obj = mojang_api_url(mciduuid)
        UUID = mojang_obj.mcid_to_uuid()
        # UUID to user profile data
        mojang_obj = mojang_api_url(UUID)
        ProfileData = mojang_obj.data_profile()
        # set date Format
        WinDate = ProfileData['timestamp'] / 1000
        FormatDate = "{0:%Y/%m/%d %H:%M:%S}".format(datetime.fromtimestamp(WinDate))

        # embed
        embed = discord.Embed(title=f"{ProfileData['profileName']}'s Profile")
        embed.set_author(name=f"{FormatDate}")
        embed.set_thumbnail(url=f"https://crafatar.com/renders/body/{ProfileData['profileId']}")
        embed.add_field(name="MCID", value=f"{ProfileData['profileName']}", inline=False)
        embed.add_field(name="UUID", value=f"{ProfileData['profileId']}", inline=False)
        # Skin
        if 'SKIN' in ProfileData['textures']:
            embed.add_field(name="SKIN", value=f"[Click here]({ProfileData['textures']['SKIN']['url']})", inline=False)
        if not 'SKIN' in ProfileData['textures']:
            embed.add_field(name="SKIN", value=f"Default", inline=False)
        # Cape
        if 'CAPE' in ProfileData['textures']:
            embed.add_field(name="Minecon Cape", value=f"[Click here]({ProfileData['textures']['CAPE']['url']})",
                            inline=False)
        if not 'CAPE' in ProfileData['textures']:
            embed.add_field(name="Minecon Cape", value=f"None", inline=False)
        embed.set_footer(text=f"{language_json['english']['embed_footer_message']}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(profile_cog(bot))
