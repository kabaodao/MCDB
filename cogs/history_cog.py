import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import math
from module import mojang_api_url, language, usagetime


# language load
class_load = language
language_json = class_load.load_language_english()


class history_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='history', invoke_without_command=True)
    async def historycommand(self, ctx, mciduuid):
        usagetime.write_usagetime("history")

        # argument(mciduuid) to UUID
        mojang_obj = mojang_api_url(mciduuid)
        UUID = mojang_obj.mcid_to_uuid()
        # UUID to user profile data
        mojang_obj = mojang_api_url(UUID)
        HistoryData = mojang_obj.data_history()

        historyLenData = len(HistoryData)
        loopcount = math.ceil((historyLenData - 1) / 10)
        l = 11
        m = 1
        n = 0
        o = 0

        embed = discord.Embed(title=f"{HistoryData[historyLenData-1]['name']}'s Name History")
        if not loopcount == 0:
            embed.set_author(name=f"Page {m}/{loopcount}")
        embed.set_footer(text=f"{language_json['english']['embed_footer_message']}")
        while n <= 10:
            if n == historyLenData:
                break
            if n < historyLenData:
                if not 'changedToAt' in HistoryData[n]:
                    embed.add_field(name=f"{n}. {HistoryData[n]['name']}", value="MCID at account creation.")
                else:
                    changedDate = HistoryData[n]['changedToAt'] / 1000
                    formatDate = "{0:%Y/%m/%d %H:%M:%S}".format(datetime.fromtimestamp(changedDate))
                    embed.add_field(name=f"{n}. {HistoryData[n]['name']}", value=f"{formatDate}", inline=False)
                n += 1
        embedmessage = await ctx.send(embed=embed)

        if historyLenData > 10:
            for n in ['\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}',
                      '\N{BLACK SQUARE FOR STOP}',
                      '\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}']:
                await embedmessage.add_reaction(n)

            def check(reaction, user):
                return user == ctx.message.author and str(
                    reaction.emoji) == '\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}' or str(
                    reaction.emoji) == '\N{BLACK SQUARE FOR STOP}' or str(
                    reaction.emoji) == '\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}' and not user.bot

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    for n in ['\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}',
                              '\N{BLACK SQUARE FOR STOP}',
                              '\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}']:
                        await embedmessage.remove_reaction(n, embedmessage.author)
                    break
                else:
                    if str(reaction) == '\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}':
                        if m == 1:
                            await embedmessage.remove_reaction(reaction, user)
                        elif m == 2:
                            n = 0
                            embed = discord.Embed(title=f"{HistoryData[historyLenData-1]['name']}'s Name History")
                            while n <= 10:
                                if n == historyLenData:
                                    break
                                if n < historyLenData:
                                    if not 'changedToAt' in HistoryData[n]:
                                        embed.add_field(name=f"{n}. {HistoryData[n]['name']}", value="MCID at account creation.")
                                    else:
                                        changedDate = HistoryData[n]['changedToAt'] / 1000
                                        formatDate = "{0:%Y/%m/%d %H:%M:%S}".format(datetime.fromtimestamp(changedDate))
                                        embed.add_field(name=f"{n}. {HistoryData[n]['name']}", value=f"{formatDate}", inline=False)
                                    n += 1
                            l -= 10
                            m -= 1
                            embed.set_author(name=f"Page {m}/{loopcount}")
                            embed.set_footer(text=f"{language_json['english']['embed_footer_message']}")
                            await embedmessage.edit(embed=embed)
                        elif m == loopcount:
                            n = 0
                            embed = discord.Embed(title=f"{HistoryData[historyLenData-1]['name']}'s Name History")
                            l -= o + 10
                            while n <= 9:
                                if l == historyLenData:
                                    break
                                if l < historyLenData:
                                    if not 'changedToAt' in HistoryData[l]:
                                        embed.add_field(name=f"{l}. {HistoryData[l]['name']}", value="MCID at account creation.")
                                    else:
                                        changedDate = HistoryData[l]['changedToAt'] / 1000
                                        formatDate = "{0:%Y/%m/%d %H:%M:%S}".format(datetime.fromtimestamp(changedDate))
                                        embed.add_field(name=f"{l}. {HistoryData[l]['name']}", value=f"{formatDate}", inline=False)
                                    l += 1
                                    n += 1
                            m -= 1
                            embed.set_author(name=f"Page {m}/{loopcount}")
                            embed.set_footer(text=f"{language_json['english']['embed_footer_message']}")
                            await embedmessage.edit(embed=embed)
                        else:
                            n = 0
                            embed = discord.Embed(title=f"{HistoryData[historyLenData-1]['name']}'s Name History")
                            await ctx.send(f"{l}")
                            l -= 10
                            await ctx.send(f"{l}")
                            while n <= 9:
                                if l == historyLenData:
                                    break
                                if l < historyLenData:
                                    if not 'changedToAt' in HistoryData[l]:
                                        embed.add_field(name=f"{l}. {HistoryData[l]['name']}", value="MCID at account creation.")
                                    else:
                                        changedDate = HistoryData[l]['changedToAt'] / 1000
                                        formatDate = "{0:%Y/%m/%d %H:%M:%S}".format(datetime.fromtimestamp(changedDate))
                                        embed.add_field(name=f"{l}. {HistoryData[l]['name']}", value=f"{formatDate}", inline=False)
                                    l += 1
                                    n += 1
                            m -= 1
                            embed.set_author(name=f"Page {m}/{loopcount}")
                            embed.set_footer(text=f"{language_json['english']['embed_footer_message']}")
                            await embedmessage.edit(embed=embed)
                        await embedmessage.remove_reaction(reaction, user)

                    elif str(reaction) == '\N{BLACK SQUARE FOR STOP}':
                        await embedmessage.remove_reaction(reaction, user)
                        for n in ['\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}',
                                  '\N{BLACK SQUARE FOR STOP}',
                                  '\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}']:
                            await embedmessage.remove_reaction(n, embedmessage.author)
                        break

                    elif str(reaction) == '\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}':
                        if m == loopcount:
                            await embedmessage.remove_reaction(reaction, user)
                        else:
                            n = 0
                            o = 0
                            embed = discord.Embed(title=f"{HistoryData[historyLenData-1]['name']}'s Name History")
                            while n <= 9:
                                if l == historyLenData:
                                    break
                                if l < historyLenData:
                                    if not 'changedToAt' in HistoryData[l]:
                                        embed.add_field(name=f"{l}. {HistoryData[l]['name']}", value="MCID at account creation.")
                                    else:
                                        changedDate = HistoryData[l]['changedToAt'] / 1000
                                        formatDate = "{0:%Y/%m/%d %H:%M:%S}".format(datetime.fromtimestamp(changedDate))
                                        embed.add_field(name=f"{l}. {HistoryData[l]['name']}", value=f"{formatDate}", inline=False)
                                    l += 1
                                    n += 1
                                    o += 1
                            m += 1
                            embed.set_author(name=f"Page {m}/{loopcount}")
                            embed.set_footer(text=f"{language_json['english']['embed_footer_message']}")
                            await embedmessage.edit(embed=embed)
                        await embedmessage.remove_reaction(reaction, user)

def setup(bot):
    bot.add_cog(history_cog(bot))