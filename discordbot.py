from discord.ext import commands
from os import getenv
import traceback
import datetime
import discord

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

    
@bot.event
async def on_vc_start(members, channel):
    now = jst()
    embed = discord.Embed(title="START log", color=discord.Color.green())
    embed.add_field(name="時刻", value=now.strftime('%Y /%m / %d　 %H : %M : %S'), inline=False)
    embed.add_field(name="開始者", value=members.name, inline=False)
    embed.add_field(name="場所", value=channel.name, inline=False)
    sent_channel = members.guild.get_channel(876478511072809010)
    embed.set_footer(icon_url = members.avatar_url, text=members.display_name)
    await sent_channel.send(embed=embed)
    member_mention = "<@&876478243111317535>"
    await sent_channel.send(f"{member_mention} 通話始まったぞ")


@bot.event
async def on_vc_end(members, channel):
    now = jst()
    embed = discord.Embed(title="END log", color=discord.Color.red())
    embed.add_field(name="時刻", value=now.strftime('%Y /%m / %d　 %H : %M : %S'), inline=False)
    embed.add_field(name="終了者", value=members.name, inline=False)
    embed.add_field(name="場所", value=channel.name, inline=False)
    sent_channel = members.guild.get_channel(876478511072809010)
    embed.set_footer(icon_url=members.avatar_url, text=members.display_name)
    await sent_channel.send(embed=embed)


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel and len(after.channel.members) == 1:
            # もし、ボイスチャットが開始されたら
            bot.dispatch("vc_start", member, after.channel)  # 発火！

        if before.channel and len(before.channel.members) == 0:
            # もし、ボイスチャットが終了したら
            bot.dispatch("vc_end", member, before.channel)  # 発火！

            
@bot.command(name="get_t_role")
async def get_t_role(ctx):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name="たかはし部－通話通知")
    await ctx.author.add_roles(role)
    msg = "付与しました！"
    await ctx.send(msg)


@bot.command(name="remove_t_role")
async def remove_t_role(ctx):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name="たかはし部－通話通知")
    await ctx.author.remove_roles(role)
    msg = "抹消しました！"
    await ctx.send(msg)         
            
            
def jst():
    now = datetime.datetime.utcnow()
    now = now + datetime.timedelta(hours=9)
    return now


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
