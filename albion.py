import discord
import requests
import time
from discord.ext import commands
from numpy import array

TValue = array([1, 2, 2, 3, 4, 5, 5])
ltime = time.asctime(time.localtime())

mineralneed = 0
beforeling = 0


def _url(self, endpoint):
    return 'https://gameinfo.albiononline.com/api/gameinfo' + endpoint


def calculoprincipal(tier, quantity, percent):
    global mineralneed
    global beforeling

    # Calcula el porcentaje de la devolucion
    calculatedpercent = (float(percent) - float(1.1)) / 100

    # Calcula el mineral a utilizar sin devolucion
    prueba = TValue[tier]
    mineral = int(quantity) * prueba

    # Calcula la devolucion por el porcentaje
    devolution = round(int(mineral) * float(calculatedpercent))

    # Calcula mineral con devolucion
    mineralneed = int(mineral) - int(devolution)

    # Calcula la cantidad de lingotes del tier anterior
    beforeling = int(quantity) - round((int(quantity) * calculatedpercent))


class albion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='register')
    async def register(self, ctx, player_name):
        embed = discord.Embed(
            title='Registro de usuario exitoso',
            description='',
            colour=discord.Colour.green()
        )

        embedW = discord.Embed(
            title='Proceso de búsqueda',
            description='',
            colour=discord.Colour.gold()
        )

        embedW.add_field(name='**Jugador**', value=player_name, inline=True)
        embedW.add_field(name='**Tiempo estimado**', value='5 segundos', inline=True)

        await ctx.send(embed=embedW)

        try:
            r = requests.get(f'https://gameinfo.albiononline.com/api/gameinfo/search?q={player_name}')
            events = r.json()
            playerName = events['players'][0]['Name']
            guildName = events['players'][0]['GuildName']
        except IndexError:
            playerName = 'null'
            guildName = 'null'

        rol = discord.utils.get(ctx.guild.roles, name="Miembro")

        print(f'[INFO {ltime}]: Jugador encontrado: {playerName}')
        print(f'[INFO {ltime}]: Gremio: {guildName}')

        if player_name == playerName:
            if guildName == 'La Federacion Y':
                print(f'[INFO {ltime}]: Jugador: {playerName} pertenece al gremio requerido')

                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Yes_Check_Circle"
                                        ".svg/1200px-Yes_Check_Circle.svg.png")
                embed.add_field(name='**Jugador**', value=playerName, inline=True)
                embed.add_field(name='**Gremio**', value=guildName, inline=True)
                embed.add_field(name='**Rol**', value=rol, inline=True)

                try:
                    await ctx.author.edit(nick=player_name)
                    await ctx.author.add_roles(rol)
                    print(f'[INFO {ltime}]: Rol y nick actualizados')
                except discord.errors.Forbidden:
                    print(f'[INFO {ltime}]: Permiso denegado')
                else:
                    await ctx.author.send("**INFO:** Bienvenido a La Federación Y: " + player_name)
                    print(f'[INFO {ltime}]: Mensaje de confirmacion enviado')
                embed.set_footer(text='Bot created by: Aguilerimon#0284')

                # await waitone.delete()
                await ctx.send(embed=embed)
            else:
                print(f'[INFO {ltime}]: El aspirante: {playerName} no pertenece al gremio requerido')

                embed = discord.Embed(title="¡El aspirante no pertenece a la guild!", color=0xfc051c)
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/148/148766.png")
                embed.add_field(name="ERROR", value="**Se ha detectado que el aspirante no ha sido "
                                                    "reclutado dentro del "
                                                    "juego. Favor "
                                                    "de contactar a un oficial para pedir su "
                                                    "ingreso a la guild.**",
                                inline=False)
                embed.set_footer(text='Bot created by: Aguilerimon#0284')
                # await waitone.delete()
                await ctx.send(embed=embed)
        elif playerName == 'null':
            print(f'[INFO {ltime}]: El aspirante: {playerName} no existe')

            embed = discord.Embed(title="¡El nombre de jugador no existe!", color=0xfc051c)
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/148/148766.png")
            embed.add_field(name="ERROR", value="**Se ha detectado que el nombre de jugador no existe en el juego. "
                                                "Favor de contactar con un administrador.**",
                            inline=False)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            # await waitone.delete()
            await ctx.send(embed=embed)
        else:
            print(f'[INFO {ltime}]: El aspirante: {playerName} no existe')

            embed = discord.Embed(title="¡El nombre de jugador no existe!", color=0xfc051c)
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/148/148766.png")
            embed.add_field(name="ERROR", value="**Se ha detectado que el nombre de jugador no existe en el juego. "
                                                "Favor de contactar con un administrador.**",
                            inline=False)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            # await waitone.delete()
            await ctx.send(embed=embed)

    @commands.command(name='refinado')
    async def refinado(self, ctx, tier, quantity, percent):
        embed = discord.Embed(
            title='Calculadora de refinado',
            description='',
            colour=discord.Colour.blue()
        )

        if tier == 'T2' or tier == 't2':
            tiervalue = 0
            tiertotal = ''
            mineraltotal = ''
            beforetotal = ''
            tierminimo = ''
            for n in range(tiervalue, -1, -1):
                calculoprincipal(n, quantity, percent)
                tiertotal += str(n + 2) + '\n'
                mineraltotal += str(mineralneed) + '\n'
                if n != 0:
                    tierminimo += str(n + 1) + '\n'
                    beforetotal += str(beforeling) + '\n'
                quantity = beforeling

            embed.add_field(name='Tier', value=tiertotal, inline=True)
            embed.add_field(name='Materiales en Bruto', value=mineraltotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            await ctx.send(embed=embed)

        elif tier == 'T3' or tier == 't3':
            tiervalue = 1
            tiertotal = ''
            mineraltotal = ''
            beforetotal = ''
            tierminimo = ''
            for n in range(tiervalue, -1, -1):
                calculoprincipal(n, quantity, percent)
                tiertotal += str(n + 2) + '\n'
                mineraltotal += str(mineralneed) + '\n'
                if n != 0:
                    tierminimo += str(n + 1) + '\n'
                    beforetotal += str(beforeling) + '\n'
                quantity = beforeling

            embed.add_field(name='Tier', value=tiertotal, inline=True)
            embed.add_field(name='Materiales en Bruto', value=mineraltotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)

            embed.add_field(name='Tier', value=tierminimo, inline=True)
            embed.add_field(name='Materiales Refinados', value=beforetotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            await ctx.send(embed=embed)

        elif tier == 'T4' or tier == 't4':
            tiervalue = 2
            tiertotal = ''
            mineraltotal = ''
            beforetotal = ''
            tierminimo = ''
            for n in range(tiervalue, -1, -1):
                calculoprincipal(n, quantity, percent)
                tiertotal += str(n + 2) + '\n'
                mineraltotal += str(mineralneed) + '\n'
                if n != 0:
                    tierminimo += str(n + 1) + '\n'
                    beforetotal += str(beforeling) + '\n'
                quantity = beforeling

            embed.add_field(name='Tier', value=tiertotal, inline=True)
            embed.add_field(name='Materiales en Bruto', value=mineraltotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)

            embed.add_field(name='Tier', value=tierminimo, inline=True)
            embed.add_field(name='Materiales Refinados', value=beforetotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            await ctx.send(embed=embed)

        elif tier == 'T5' or tier == 't5':
            tiervalue = 3
            tiertotal = ''
            mineraltotal = ''
            beforetotal = ''
            tierminimo = ''
            for n in range(tiervalue, -1, -1):
                calculoprincipal(n, quantity, percent)
                tiertotal += str(n + 2) + '\n'
                mineraltotal += str(mineralneed) + '\n'
                if n != 0:
                    tierminimo += str(n + 1) + '\n'
                    beforetotal += str(beforeling) + '\n'
                quantity = beforeling

            embed.add_field(name='Tier', value=tiertotal, inline=True)
            embed.add_field(name='Materiales en Bruto', value=mineraltotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)

            embed.add_field(name='Tier', value=tierminimo, inline=True)
            embed.add_field(name='Materiales Refinados', value=beforetotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            await ctx.send(embed=embed)

        elif tier == 'T6' or tier == 't6':
            tiervalue = 4
            tiertotal = ''
            mineraltotal = ''
            beforetotal = ''
            tierminimo = ''
            for n in range(tiervalue, -1, -1):
                calculoprincipal(n, quantity, percent)
                tiertotal += str(n + 2) + '\n'
                mineraltotal += str(mineralneed) + '\n'
                if n != 0:
                    tierminimo += str(n + 1) + '\n'
                    beforetotal += str(beforeling) + '\n'
                quantity = beforeling

            embed.add_field(name='Tier', value=tiertotal, inline=True)
            embed.add_field(name='Materiales en Bruto', value=mineraltotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)

            embed.add_field(name='Tier', value=tierminimo, inline=True)
            embed.add_field(name='Materiales Refinados', value=beforetotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            await ctx.send(embed=embed)

        elif tier == 'T7' or tier == 't7':
            tiervalue = 5
            tiertotal = ''
            mineraltotal = ''
            beforetotal = ''
            tierminimo = ''
            for n in range(tiervalue, -1, -1):
                calculoprincipal(n, quantity, percent)
                tiertotal += str(n + 2) + '\n'
                mineraltotal += str(mineralneed) + '\n'
                if n != 0:
                    tierminimo += str(n + 1) + '\n'
                    beforetotal += str(beforeling) + '\n'
                quantity = beforeling

            embed.add_field(name='Tier', value=tiertotal, inline=True)
            embed.add_field(name='Materiales en Bruto', value=mineraltotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)

            embed.add_field(name='Tier', value=tierminimo, inline=True)
            embed.add_field(name='Materiales Refinados', value=beforetotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            await ctx.send(embed=embed)

        elif tier == 'T8' or tier == 't8':
            tiervalue = 6
            tiertotal = ''
            mineraltotal = ''
            beforetotal = ''
            tierminimo = ''
            for n in range(tiervalue, -1, -1):
                calculoprincipal(n, quantity, percent)
                tiertotal += str(n + 2) + '\n'
                mineraltotal += str(mineralneed) + '\n'
                if n != 0:
                    tierminimo += str(n + 1) + '\n'
                    beforetotal += str(beforeling) + '\n'
                quantity = beforeling

            embed.add_field(name='Tier', value=tiertotal, inline=True)
            embed.add_field(name='Materiales en Bruto', value=mineraltotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)

            embed.add_field(name='Tier', value=tierminimo, inline=True)
            embed.add_field(name='Materiales Refinados', value=beforetotal, inline=True)
            embed.add_field(name='Porcentaje de devolucion', value=percent + '%', inline=True)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error - Comando refinado", color=0xfc051c)
            embed.add_field(name="Error en el tier valido",
                            value="El rango de tiers validos para el calculo es de: T2 a "
                                  "T8.**", inline=False)
            embed.add_field(name="Ejemplo", value="!refinado **T5** 900 36.7", inline=False)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            await ctx.send(embed=embed)

    @refinado.error
    async def refinado_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="Error - Comando refinado", color=0xfc051c)
            embed.add_field(name="Error de sintaxis",
                            value="La sintaxis correcta es: **!refinado [tier] [cantidad] ["
                                  "devolucion].**", inline=False)
            embed.add_field(name="Ejemplo", value="**!refinado T5 900 36.7**", inline=False)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            await ctx.send(embed=embed)

    @register.error
    async def register_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            embed = discord.Embed(title="Error - Comando register", color=0xfc051c)
            embed.add_field(name="Error de sintaxis",
                            value="La sintaxis correcta es: **!register [NamePlayer].**", inline=False)
            embed.add_field(name="Ejemplo", value="**!register FluffyLamb**", inline=False)
            embed.set_footer(text='Bot created by: Aguilerimon#0284')
            await ctx.send(embed=embed)
