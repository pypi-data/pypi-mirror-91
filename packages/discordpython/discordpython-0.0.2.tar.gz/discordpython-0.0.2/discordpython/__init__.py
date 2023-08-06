import discord
from discord.ext import commands
import pkg_resources
from datetime import datetime
import humanize
import os


class Python(commands.Cog):

  def __init__(self,bot):
    self.bot=bot
    self.load_time=datetime.now()



  @commands.command()
  async def pkg_version(self,ctx,*,package):
    try:
        await ctx.send(pkg_resources.get_distribution(package).version)
    except (pkg_resources.DistributionNotFound, AttributeError):
        await ctx.send("You have not imported this module")
  @commands.group()
  #@commands.is_owner()
  async def python(self,ctx):
    if ctx.invoked_subcommand is None:
      embed=discord.Embed(colour=0xF000E5)
      embed.add_field(name="Cog!",value="""Python Cog:
Written by: Der Herbst#2365
Maintained by: Der Herbst#2365
discord.py version: """+pkg_resources.get_distribution("discord.py").version+"""
Cog loaded: """+humanize.naturaltime(self.load_time))
      await ctx.send(embed=embed)
  @python.command()
  @commands.is_owner()
  async def load(self,ctx,*,extension):
    #try:
    self.bot.load_extension(extension)
    #except:
      #await ctx.send(f"Sorry but the extension {extension} does not exist.")
    await ctx.send(f"📥 Loaded Cog {extension}")

  @python.command()
  @commands.is_owner()
  async def reload(self,ctx,*,extension):
    self.bot.reload_extension(extension)
    await ctx.send(f"📥 Reloaded Cog {extension}")
  @python.command()
  @commands.is_owner()
  async def unload(self,ctx,*,extension):
    self.bot.unload_extension(extension)
    await ctx.send(f"📤 Unloaded Cog {extension}")
  @python.command()
  async def kgs(self,ctx,*,sentence):
    #await ctx.channel.purge(limit=1)
    f=open("message.txt","w+")
    f.write(sentence)
    f.close()
    file=discord.File("message.txt")
    await ctx.send(file=file)
    os.remove("message.txt")
  @python.command()
  async def state(self,ctx,member:discord.Member):
    await ctx.send(f"""```py
    import {member.display_name}
    from {member.display_name}.ext import commands
    client=commands.Bot(command_prefix=\"{member.display_name}\"
    @client.command()
    async def ping(ctx):
      await ctx.send(\"Pong!\")
    client.run(\"TOKEN\")
    ```""")
  @python.command()
  async def get_command(self,ctx,command_check):
    lst=[]
    for command in self.bot.commands:
      lst.append(command.name)
    if command_check in lst:
      await ctx.send("The command `"+command_check+"` is a valid command.")
    if command_check not in lst:
      await ctx.send("Could not find command: `"+command_check+"` :frowning:")

def setup(bot):
  bot.add_cog(Python(bot))