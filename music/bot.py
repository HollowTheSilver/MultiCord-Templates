#!/usr/bin/env python3
"""
Music Discord Bot Template for MultiCord.
A simple music bot with basic playback features.
Note: Requires additional setup for audio playback (FFmpeg, youtube-dl/yt-dlp).
"""

import os
import sys
import logging
from pathlib import Path
import discord
from discord.ext import commands
from datetime import datetime
import toml
import asyncio

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load configuration
config_path = Path(__file__).parent / "config.toml"
if config_path.exists():
    with open(config_path) as f:
        config = toml.load(f)
else:
    logger.error("config.toml not found!")
    sys.exit(1)

# Bot configuration
TOKEN = config["bot"]["token"]
PREFIX = config["bot"].get("prefix", "!")
DESCRIPTION = config["bot"].get("description", "A music Discord bot")

# Intents configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

class MusicBot(commands.Bot):
    """Music Discord bot with MultiCord integration."""
    
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            description=DESCRIPTION,
            intents=intents,
            help_command=commands.DefaultHelpCommand()
        )
        self.start_time = datetime.utcnow()
        self.bot_name = os.environ.get('BOT_NAME', 'music-bot')
        self.bot_port = os.environ.get('BOT_PORT', '8100')
        
        # Music queue per guild
        self.music_queues = {}  # {guild_id: [songs]}
        
    async def on_ready(self):
        """Event triggered when bot is ready."""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
        
        # Set status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=f"{PREFIX}play | {PREFIX}help"
            )
        )

# Create bot instance
bot = MusicBot()

# Music commands
@bot.command(name='join', aliases=['connect'])
async def join(ctx):
    """Join the voice channel of the message author."""
    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to use this command!")
        return
    
    channel = ctx.author.voice.channel
    
    if ctx.voice_client:
        if ctx.voice_client.channel == channel:
            await ctx.send(f"I'm already in {channel.mention}!")
            return
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    
    await ctx.send(f"Connected to {channel.mention}")
    logger.info(f"Joined voice channel: {channel.name} in {ctx.guild.name}")

@bot.command(name='leave', aliases=['disconnect', 'dc'])
async def leave(ctx):
    """Leave the voice channel."""
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel!")
        return
    
    await ctx.voice_client.disconnect()
    
    # Clear queue for this guild
    if ctx.guild.id in bot.music_queues:
        bot.music_queues[ctx.guild.id].clear()
    
    await ctx.send("Disconnected from voice channel")
    logger.info(f"Left voice channel in {ctx.guild.name}")

@bot.command(name='play', aliases=['p'])
async def play(ctx, *, query: str):
    """Play a song (simplified - requires additional implementation)."""
    # Ensure bot is in voice channel
    if not ctx.voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You need to be in a voice channel!")
            return
    
    # This is a simplified version - in production you'd use youtube-dl/yt-dlp
    # to search and download the audio
    
    embed = discord.Embed(
        title="Added to Queue",
        description=f"🎵 {query}",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Requested by {ctx.author}")
    
    await ctx.send(embed=embed)
    
    # Add to queue
    if ctx.guild.id not in bot.music_queues:
        bot.music_queues[ctx.guild.id] = []
    bot.music_queues[ctx.guild.id].append({
        'title': query,
        'requester': str(ctx.author)
    })
    
    logger.info(f"Added '{query}' to queue in {ctx.guild.name}")

@bot.command(name='pause')
async def pause(ctx):
    """Pause the current playback."""
    if not ctx.voice_client or not ctx.voice_client.is_playing():
        await ctx.send("Nothing is playing!")
        return
    
    ctx.voice_client.pause()
    await ctx.send("⏸️ Paused playback")

@bot.command(name='resume')
async def resume(ctx):
    """Resume the paused playback."""
    if not ctx.voice_client or not ctx.voice_client.is_paused():
        await ctx.send("Nothing is paused!")
        return
    
    ctx.voice_client.resume()
    await ctx.send("▶️ Resumed playback")

@bot.command(name='stop')
async def stop(ctx):
    """Stop playback and clear the queue."""
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel!")
        return
    
    if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
        ctx.voice_client.stop()
    
    # Clear queue
    if ctx.guild.id in bot.music_queues:
        bot.music_queues[ctx.guild.id].clear()
    
    await ctx.send("⏹️ Stopped playback and cleared queue")

@bot.command(name='skip', aliases=['s'])
async def skip(ctx):
    """Skip the current song."""
    if not ctx.voice_client or not ctx.voice_client.is_playing():
        await ctx.send("Nothing is playing!")
        return
    
    ctx.voice_client.stop()
    await ctx.send("⏭️ Skipped current song")

@bot.command(name='queue', aliases=['q'])
async def queue(ctx):
    """Display the music queue."""
    if ctx.guild.id not in bot.music_queues or not bot.music_queues[ctx.guild.id]:
        await ctx.send("The queue is empty!")
        return
    
    queue_list = bot.music_queues[ctx.guild.id]
    
    embed = discord.Embed(
        title="Music Queue",
        color=discord.Color.blue()
    )
    
    for i, song in enumerate(queue_list[:10], 1):  # Show first 10
        embed.add_field(
            name=f"{i}. {song['title']}",
            value=f"Requested by {song['requester']}",
            inline=False
        )
    
    if len(queue_list) > 10:
        embed.set_footer(text=f"And {len(queue_list) - 10} more...")
    
    await ctx.send(embed=embed)

@bot.command(name='nowplaying', aliases=['np'])
async def nowplaying(ctx):
    """Show the currently playing song."""
    if not ctx.voice_client or not ctx.voice_client.is_playing():
        await ctx.send("Nothing is playing!")
        return
    
    # This would show actual playing info in a real implementation
    embed = discord.Embed(
        title="Now Playing",
        description="🎵 Current song information would appear here",
        color=discord.Color.purple()
    )
    
    await ctx.send(embed=embed)

@bot.command(name='volume', aliases=['vol'])
async def volume(ctx, volume: int):
    """Adjust the volume (0-100)."""
    if not ctx.voice_client:
        await ctx.send("I'm not in a voice channel!")
        return
    
    if not 0 <= volume <= 100:
        await ctx.send("Volume must be between 0 and 100!")
        return
    
    # In a real implementation, you'd adjust the actual volume here
    await ctx.send(f"🔊 Volume set to {volume}%")
    logger.info(f"Volume set to {volume}% in {ctx.guild.name}")

# Error handling
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors."""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Invalid argument: {error}")
    else:
        logger.error(f"Error in command {ctx.command}: {error}")
        await ctx.send("An error occurred while processing this command.")

if __name__ == "__main__":
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    # Check for FFmpeg (required for audio)
    try:
        import shutil
        if not shutil.which("ffmpeg"):
            logger.warning("FFmpeg not found! Audio playback will not work.")
            logger.warning("Please install FFmpeg: https://ffmpeg.org/download.html")
    except:
        pass
    
    # Run the bot
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid bot token! Please check your config.toml")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)