import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_USER_ID = None
NOGIF_MODE = False
ADMIN_IDS = [123456789012345678]  # <-- Put your Discord ID(s) here

def is_admin(ctx):
    return ctx.author.id in ADMIN_IDS

@bot.event
async def on_message(message):
    global TARGET_USER_ID, NOGIF_MODE
    if message.author == bot.user:
        return
    if NOGIF_MODE and TARGET_USER_ID and message.author.id == TARGET_USER_ID:
        for attachment in message.attachments:
            if attachment.url.endswith('.gif'):
                await message.delete()
                return
        for embed in message.embeds:
            if (embed.url and '.gif' in embed.url) or (embed.description and '.gif' in embed.description):
                await message.delete()
                return
        if '.gif' in message.content or 'tenor.com/view' in message.content or 'giphy.com/gifs' in message.content:
            await message.delete()
            return
    await bot.process_commands(message)

@bot.command(name='nogif')
async def nogif(ctx, user: discord.Member):
    if not is_admin(ctx):
        await ctx.send("You do not have permission to use this command!")
        return
    global TARGET_USER_ID, NOGIF_MODE
    TARGET_USER_ID = user.id
    NOGIF_MODE = True
    await ctx.send(f"GIF deletion enabled for: {user.mention}")

@bot.command(name='okgif')
async def okgif(ctx):
    if not is_admin(ctx):
        await ctx.send("You do not have permission to use this command!")
        return
    global NOGIF_MODE
    NOGIF_MODE = False
    await ctx.send("GIF deletion disabled.")

if __name__ == '__main__':
    bot.run("DISCORD_TOKEN"))
