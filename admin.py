import discord
from discord.ext import commands
from typing import Optional


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def info_refinado(self, ctx):
        embed = discord.Embed(description="Devuelve una tabla la cual indica la cantidad de material bruto y refinado "
                                          "necesita para sus jornadas de refinamiento.", color=0xff80ff)
        embed.add_field(name="Sintaxis:", value="`!refinado [tier] [cantidad] ["
                                                "devolucion]`", inline=False)
        embed.set_footer(text='Bot created by: Aguilerimon#0284')
        await ctx.send(embed=embed)

    async def info_register(self, ctx):
        embed = discord.Embed(description="Envia una solicitud de ingreso que asigna el rol correspondiente al recluta.", color=0xff80ff)
        embed.add_field(name="Sintaxis:", value="`!register [NamePlayer]`", inline=False)
        embed.set_footer(text='Bot created by: Aguilerimon#0284')
        await ctx.send(embed=embed)

    async def info_limpiar(self, ctx):
        embed = discord.Embed(description="Elimina una cantidad de mensajes en un canal, "
                                          "la cantida maxima es: `100`.", color=0xff80ff)
        embed.set_author(name=f'{"Administración: limpiar"}', icon_url=f'{self.bot.user.avatar_url}')
        embed.add_field(name="Sintaxis:", value="`!limpiar [cantidad]`", inline=False)
        embed.set_footer(text='Bot created by: Aguilerimon#0284')
        await ctx.send(embed=embed)

    @commands.command(name="limpiar")
    async def limpiar(self, ctx, arg):
        amount = 5
        try:
            amount = int(arg)
        except Exception:
            pass
        await ctx.channel.purge(limit=amount)

    @limpiar.error
    async def limpiar_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="Error - Comando limpiar", color=0xfc051c)
            embed.add_field(name="!ERROR!", value="**Debes añadir la cantidad de mensajes a eliminar.**",
                            inline=False)
            embed.add_field(name="Ejemplo de Sintaxis", value="`!limpiar [cantidad]`", inline=False)
            await ctx.send(embed=embed)

    @commands.command(name='ayuda')
    async def ayuda(self, ctx, cmd: Optional[str]):
        if cmd is None:
            embed = discord.Embed(description="Bienvenido a la sección de ayuda de Federación Bot.", color=0xff80ff)
            embed.set_author(name=f'{"Lista de comandos de Federación Bot"}', icon_url=f'{self.bot.user.avatar_url}')

            embed.add_field(name="Administración", value="`limpiar`", inline=False)

            embed.add_field(name="Albion", value="`refinado` `register`", inline=False)

            embed.set_footer(text="Si requieres información detallada de algun comando: !ayuda [comando]")

            await ctx.send(embed=embed)
        else:
            if cmd == 'refinado':
                await self.info_refinado(ctx)

            elif cmd == 'register':
                await self.info_register(ctx)

            elif cmd == "limpiar":
                await self.info_limpiar(ctx)

            else:
                await ctx.send("❌ El comando no existe ❌")
