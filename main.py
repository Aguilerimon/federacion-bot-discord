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
        await bot.change_presence(activity=discord.Game(name='Warframe | v1.1'))
        # await asyncio.sleep(5)
        # await bot.change_presence(activity=discord.Game(name='happy ayudita'))
        # await asyncio.sleep(5)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="¡Error! ¡HappyBot esta triste!", color=0xfc051c)
        embed.add_field(name="Error en la Matrix", value="**Te equivocaste de comando... Idiota!.**",
                        inline=False)
        embed.set_image(url='https://i.pinimg.com/originals/4f/b4/04/4fb4040f32a0686a41ace938165bfe5a.gif')
        await ctx.send(embed=embed)


# ---------------------------- COMANDO RULE34 -----------------------------
bot.add_cog(albion(bot))
# -------------------------------------------------------------------------
# ---------------------------- COMANDO RULE34 -----------------------------
bot.add_cog(admin(bot))
# -------------------------------------------------------------------------

bot.run(os.environ['TOKEN'])
