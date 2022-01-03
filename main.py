import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

class MyClient(discord.Client):
  
  async def on_ready(self):
    activity = discord.Game(name="Bread Baking Simulator", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)
    print('[System] Logged on as', self.user)
    print('[System] Running version 1.0')

  async def on_message(self, message):
    if message.author == self.user:
      return

    if message.content == 'Bread 👍':
      await message.channel.send('Bread 👍')
      print('[Event handler] "Bread 👍" event handled')

    if message.content == "LOL":
      await message.channel.send(file=discord.File('gif/cereal_dude.gif'))
      print('[Event handler] "LOL" event handled')

    if message.content == "gtfo dude":
      await message.channel.send(file=discord.File('gif/gtfo_bro.gif'))
      print('[Event handler] "fuck niggas" event handled')

    if message.content == "good night homie 🙂":
      await message.channel.send(file=discord.File('gif/ayaya_bye.gif'))
      print('[Event handler] "good night homie :)" event handled')

    if message.content == "get good bitch":
      await message.channel.send(file=discord.File('gif/get_good_retard.gif'))
      print('[Event handler] "get good retard" event handled')

    if message.content == "Realtek17":
      embed=discord.Embed(title="🤖 Bot status")
      embed.add_field(name="🔴 Ping: ", value=client.latency*1000, inline=False)
      embed.add_field(name="⏱️  Runtime:", value="it brokie", inline=False)
      embed.add_field(name="🖥️ Hosting: ", value="repl.it patch ur servers hahs", inline=False)
      await message.channel.send(embed=embed)
      print('[Event handler] "Realtek17" event handled')

client = MyClient()
keep_alive()
client.run(os.getenv('TOKEN'))