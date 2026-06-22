import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

import os
import random
import re

# --------------------
# Setup
# --------------------

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# --------------------
# Storage
# --------------------

edit_snipes = {}

# --------------------
# Startup
# --------------------

@bot.event
async def on_ready():

    try:

        synced = await bot.tree.sync()

        print(
            f"Synced {len(synced)} slash commands"
        )

    except Exception as e:

        print(
            f"Sync Error: {e}"
        )

    print(
        f"{bot.user} is online!"
    )

# --------------------
# Edit Tracking
# --------------------

@bot.event
async def on_message_edit(
    before,
    after
):

    if before.author.bot:
        return

    if before.content == after.content:
        return

    edit_snipes[
        before.channel.id
    ] = {

        "author": before.author,

        "before": (
            before.content
            if before.content
            else "*empty*"
        ),

        "after": (
            after.content
            if after.content
            else "*empty*"
        )
    }

# --------------------
# /hello
# --------------------

@bot.tree.command(
    name="hello",
    description="Say hello"
)
async def hello(
    interaction: discord.Interaction
):

    await interaction.response.send_message(
        f"Hello {interaction.user.mention}! 🦈",
        ephemeral=True
    )

# --------------------
# /ping
# --------------------

@bot.tree.command(
    name="ping",
    description="Check bot latency"
)
async def ping(
    interaction: discord.Interaction
):

    latency = round(
        bot.latency * 1000
    )

    await interaction.response.send_message(
        f"🏓 Pong! {latency}ms",
        ephemeral=True
    )

# --------------------
# /coinflip
# --------------------

@bot.tree.command(
    name="coinflip",
    description="Flip a coin"
)
async def coinflip(
    interaction: discord.Interaction
):

    result = random.choice(
        [
            "Heads",
            "Tails"
        ]
    )

    await interaction.response.send_message(
        f"🪙 {result}",
    )

# --------------------
# /roll
# --------------------

@bot.tree.command(
    name="roll",
    description="Roll a dice"
)
@app_commands.describe(
    sides="Number of sides"
)
async def roll(
    interaction: discord.Interaction,
    sides: int = 6
):

    if sides < 2:

        await interaction.response.send_message(
            "Dice must have at least 2 sides.",
            ephemeral=True
        )

        return

    result = random.randint(
        1,
        sides
    )

    await interaction.response.send_message(
        f"🎲 {result}",
    )

# --------------------
# /eightball
# --------------------

@bot.tree.command(
    name="eightball",
    description="Ask the magic 8-ball"
)
@app_commands.describe(
    question="Your question"
)
async def eightball(
    interaction: discord.Interaction,
    question: str
):

    responses = [

        "Yes.",
        "No.",
        "Maybe.",
        "Definitely.",
        "Probably.",
        "Very unlikely.",
        "Ask again later.",
        "Without a doubt.",
        "Absolutely.",
        "Signs point to yes.",
        "I wouldn't count on it.",
        "Outlook good.",
        "Reply hazy."
    ]

    await interaction.response.send_message(
        f"🎱 Question:\n"
        f"`{question}`\n\n"
        f"Answer:\n"
        f"**{random.choice(responses)}**",
    )

# --------------------
# /avatar
# --------------------

@bot.tree.command(
    name="avatar",
    description="View and download a user's avatar"
)
async def avatar(
    interaction: discord.Interaction,
    member: discord.Member = None
):

    member = member or interaction.user

    avatar_url = (
        member.display_avatar
        .replace(size=4096)
        .url
    )

    embed = discord.Embed(
        title=f"{member.display_name}'s Avatar",
        color=discord.Color.blue()
    )

    embed.set_image(
        url=avatar_url
    )

    embed.add_field(
        name="Download",
        value=f"[Open Avatar]({avatar_url})",
        inline=False
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )

# --------------------
# /emojisteal
# --------------------

@bot.tree.command(
    name="emojisteal",
    description="Get a downloadable emoji image"
)
async def emojisteal(
    interaction: discord.Interaction,
    emoji: str
):

    match = re.match(
        r"<(a?):(\w+):(\d+)>",
        emoji
    )

    if not match:

        await interaction.response.send_message(
            "Please provide a valid custom emoji.",
            ephemeral=True
        )

        return

    animated = bool(
        match.group(1)
    )

    name = match.group(2)

    emoji_id = match.group(3)

    ext = (
        "gif"
        if animated
        else "png"
    )

    url = (
        f"https://cdn.discordapp.com/emojis/"
        f"{emoji_id}.{ext}"
        f"?size=4096&quality=lossless"
    )

    embed = discord.Embed(
        title=(
            f"{'Animated Emoji' if animated else 'Emoji'}"
            f": {name}"
        ),
        color=discord.Color.blurple()
    )

    embed.set_image(
        url=url
    )

    embed.add_field(
        name="Download",
        value=f"[Open in Browser]({url})",
        inline=False
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )

# --------------------
# /userinfo
# --------------------

@bot.tree.command(
    name="userinfo",
    description="View information about a user"
)
@app_commands.describe(
    member="Member to inspect"
)
async def userinfo(
    interaction: discord.Interaction,
    member: discord.Member = None
):

    member = member or interaction.user

    joined = (
        member.joined_at.strftime(
            "%Y-%m-%d"
        )
        if member.joined_at
        else "Unknown"
    )

    embed = discord.Embed(
        title=str(member),
        color=discord.Color.blue()
    )

    embed.add_field(
        name="User ID",
        value=member.id,
        inline=False
    )

    embed.add_field(
        name="Joined Server",
        value=joined,
        inline=False
    )

    embed.set_thumbnail(
        url=member.display_avatar.url
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )

# --------------------
# /serverinfo
# --------------------

@bot.tree.command(
    name="serverinfo",
    description="View server information"
)
async def serverinfo(
    interaction: discord.Interaction
):

    guild = interaction.guild

    embed = discord.Embed(
        title=guild.name,
        color=discord.Color.green()
    )

    embed.add_field(
        name="Members",
        value=guild.member_count,
        inline=True
    )

    embed.add_field(
        name="Owner",
        value=str(guild.owner),
        inline=True
    )

    if guild.icon:

        embed.set_thumbnail(
            url=guild.icon.url
        )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )

# --------------------
# /nickname
# --------------------

@bot.tree.command(
    name="nickname",
    description="Generate an Xbox-style gamertag"
)
async def nickname(
    interaction: discord.Interaction
):

    first = [

        "Shadow",
        "Ghost",
        "Crimson",
        "Turbo",
        "Nova",
        "Void",
        "Arctic",
        "Rapid",
        "Pixel",
        "Omega",
        "Silent",
        "Epic",
        "Cyber",
        "Lucky",
        "Steel"
    ]

    second = [

        "Wolf",
        "Dragon",
        "Shark",
        "Knight",
        "Ninja",
        "Penguin",
        "Tiger",
        "Otter",
        "Phoenix",
        "Beast",
        "Legend",
        "Monkey",
        "Wizard",
        "Hunter"
    ]

    styles = [

        lambda:
            f"{random.choice(first)}"
            f"{random.choice(second)}"
            f"{random.randint(10,9999)}",

        lambda:
            f"xX{random.choice(first)}"
            f"{random.choice(second)}Xx",

        lambda:
            f"The{random.choice(second)}"
            f"{random.randint(1,999)}",

        lambda:
            f"{random.choice(first)}"
            f"_{random.choice(second)}",

        lambda:
            f"ii{random.choice(first)}"
            f"{random.choice(second)}"
    ]

    gamertag = random.choice(
        styles
    )()

    await interaction.response.send_message(
        f"🎮 Generated Gamertag:\n"
        f"`{gamertag}`",
        ephemeral=True
    )

# --------------------
# /editsnipe
# --------------------

@bot.tree.command(
    name="editsnipe",
    description="View the most recently edited message"
)
async def editsnipe(
    interaction: discord.Interaction
):

    data = edit_snipes.get(
        interaction.channel.id
    )

    if not data:

        await interaction.response.send_message(
            "No edited messages found.",
            ephemeral=True
        )

        return

    embed = discord.Embed(
        title="✏️ Last Edited Message",
        color=discord.Color.orange()
    )

    embed.add_field(
        name="Author",
        value=data["author"].mention,
        inline=False
    )

    embed.add_field(
        name="Before",
        value=data["before"][:1024],
        inline=False
    )

    embed.add_field(
        name="After",
        value=data["after"][:1024],
        inline=False
    )

    await interaction.response.send_message(
        embed=embed,
        ephemeral=True
    )

bot.run(TOKEN)
