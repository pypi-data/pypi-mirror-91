import discord
from discord.ext import commands

import chat_exporter

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Live: ", {bot.user.name})
    chat_exporter.init_exporter(bot)


@bot.command()
async def embed(ctx):
    embed = discord.Embed(
        title="**__[hi](https://www.google.com)__**",
        description="**__[hi](https://www.google.com)__**",
        colour=discord.Colour.blue()
    )

    embed.add_field(name="**__https://www.google.com__**", value="**__https://www.google.com__**")
    embed.add_field(name="```hi```", value="```hi```", inline=True)
    embed.add_field(name="`hi`", value="`hi`", inline=False)
    embed.set_author(name="https://www.google.com")
    embed.set_footer(text="https://www.google.com")
    await ctx.send(embed=embed)


@bot.command()
async def save(ctx):
    await chat_exporter.quick_export(ctx)


if __name__ == "__main__":
    # bot.run("NjQ0MTQ5MTkxNTI1NzkzODUy.Xcv0rg.Lna_MP5CDWcU0aWZ0y86pZFcJIQ")  # watermelon
    bot.run("NzkyNjMwMzY0MzE2NzYyMTMy.X-ggjQ.DWhixEYx3ymZVGriT1m91LuoQhA")
