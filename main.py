import discord
import time
import os

from albion import albion
from admin import admin

from discord.ext import commands

bot = commands.Bot(command_prefix='!')

ltime = time.asctime(time.localtime())


@bot.event
async def on_ready():
    print(f'[INFO {ltime}]: Logged in as {bot.user.name}!')
    await statuschange()


async def statuschange():
    while True:
        await bot.change_presence(activity=discord.Game(name='!ayuda'))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Error General", color=0xfc051c)
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/148/148766.png")
        embed.add_field(name="Error", value="**El comando no existe.**",
                        inline=False)
        await ctx.send(embed=embed)


# ---------------------------- COMANDO RULE34 -----------------------------
bot.add_cog(albion(bot))
# -------------------------------------------------------------------------
# ---------------------------- COMANDO RULE34 -----------------------------
bot.add_cog(admin(bot))
# -------------------------------------------------------------------------

bot.run(os.environ['TOKEN'])
