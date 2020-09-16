import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
import boto3
import os


# JST time
JST = timezone(timedelta(hours=+9), 'JST')
dt = datetime.now(JST)
JSTdt = dt.isoformat(' ', 'seconds')

# aws s3
s3 = boto3.resource(
    's3',
    region_name='ap-northeast-1',
    aws_access_key_id=os.environ["AWS_S3_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_S3_SECRET_ACCESS_KEY"]
)

client = commands.Bot(command_prefix="m.")
client.remove_command("help")


# run event
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="m.help"))
    print(client.user.name)
    s3.Bucket(os.environ["AWS_S3_BUCKET_NAME"]).download_file("command_usagetime.json", "json/command_usagetime.json")


# error event
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.channel.send("Please pass in argument.")

    if isinstance(error, commands.CommandNotFound):
        await ctx.message.channel.send("Command not found.")

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission.")

    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("MCID/UUID not found.")


# cogs load
extensions = ['cogs.help_cog', 'cogs.history_cog', 'cogs.profile_cog', 'cogs.status_cog']
if __name__ == "__main__":
    for ext in extensions:
        client.load_extension(ext)


# loop
@tasks.loop(hours=1)
async def loop():
    print(f"loop upload - {JSTdt}")
    s3.Bucket(os.environ["AWS_S3_BUCKET_NAME"]).upload_file("json/command_usagetime.json", "command_usagetime.json")


loop.start()
client.run(os.environ["DISCORDBOT_TOKEN"])
