from discord.ext import commands
from os import getenv
import traceback

bot = commands.Bot(command_prefix='/')


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

    
@bot.event
async def on_vc_start(member, channel):
    print(f"{member.name}が{channel.name}でボイスチャットを開始しました。")


@bot.event
async def on_vc_end(member, channel):
    print(f"{member.name}が{channel.name}のボイスチャットを終了しました。")


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel and len(after.channel.members) == 1:
            # もし、ボイスチャットが開始されたら
            bot.dispatch("vc_start", member, after.channel)  # 発火！

        if before.channel and len(before.channel.members) == 0:
            # もし、ボイスチャットが終了したら
            bot.dispatch("vc_end", member, before.channel)  # 発火！

            
token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
