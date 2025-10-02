#!/usr/bin/env python3
"""
Basic Discord Bot Template for MultiCord.
A simple, extensible Discord bot with command handling.
"""

import os
import sys
import logging
from pathlib import Path
import discord
from discord.ext import commands
from datetime import datetime
import toml

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
DESCRIPTION = config["bot"].get("description", "A basic Discord bot")

# Intents configuration
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

class BasicBot(commands.Bot):
    """Basic Discord bot with MultiCord integration."""
    
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            description=DESCRIPTION,
            intents=intents,
            help_command=commands.DefaultHelpCommand()
        )
        self.start_time = datetime.utcnow()
        self.bot_name = os.environ.get('BOT_NAME', 'basic-bot')
        self.bot_port = os.environ.get('BOT_PORT', '8100')
        
    async def setup_hook(self):
        """Setup hook for bot initialization."""
        logger.info(f"Setting up {self.bot_name} on port {self.bot_port}")
        
        # Load cogs
        await self.load_extensions()
        
    async def load_extensions(self):
        """Load bot extensions/cogs."""
        cogs_dir = Path(__file__).parent / "cogs"
        if cogs_dir.exists():
            for cog_file in cogs_dir.glob("*.py"):
                if cog_file.stem != "__init__":
                    try:
                        await self.load_extension(f"cogs.{cog_file.stem}")
                        logger.info(f"Loaded cog: {cog_file.stem}")
                    except Exception as e:
                        logger.error(f"Failed to load cog {cog_file.stem}: {e}")
    
    async def on_ready(self):
        """Event triggered when bot is ready."""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
        
        # Set status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.guilds)} servers | {PREFIX}help"
            )
        )
        
    async def on_guild_join(self, guild):
        """Event triggered when bot joins a guild."""
        logger.info(f'Joined guild: {guild.name} (ID: {guild.id})')
        
    async def on_guild_remove(self, guild):
        """Event triggered when bot leaves a guild."""
        logger.info(f'Left guild: {guild.name} (ID: {guild.id})')
        
    async def on_command_error(self, ctx, error):
        """Global error handler for commands."""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Invalid argument provided: {error}")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Command on cooldown. Try again in {error.retry_after:.1f}s")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        else:
            logger.error(f"Unhandled error in command {ctx.command}: {error}")
            await ctx.send("An error occurred while processing this command.")

# Create bot instance
bot = BasicBot()

# Basic commands
@bot.command(name='ping')
async def ping(ctx):
    """Check bot latency."""
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! Latency: {latency}ms')

@bot.command(name='uptime')
async def uptime(ctx):
    """Check bot uptime."""
    delta = datetime.utcnow() - bot.start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    
    uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    await ctx.send(f'Bot uptime: {uptime_str}')

@bot.command(name='stats')
async def stats(ctx):
    """Display bot statistics."""
    embed = discord.Embed(
        title="Bot Statistics",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(bot.users), inline=True)
    embed.add_field(name="Commands", value=len(bot.commands), inline=True)
    embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms", inline=True)
    
    delta = datetime.utcnow() - bot.start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)
    embed.add_field(name="Uptime", value=f"{hours}h {minutes}m", inline=True)
    
    embed.set_footer(text=f"MultiCord Bot: {bot.bot_name}")
    
    await ctx.send(embed=embed)

@bot.command(name='info')
async def info(ctx):
    """Display bot information."""
    embed = discord.Embed(
        title=bot.user.name,
        description=bot.description,
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="About",
        value="This is a basic Discord bot template powered by MultiCord.",
        inline=False
    )
    
    embed.add_field(name="Prefix", value=PREFIX, inline=True)
    embed.add_field(name="Version", value="1.0.0", inline=True)
    embed.add_field(name="Library", value=f"discord.py {discord.__version__}", inline=True)
    
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
    embed.set_footer(text="Made with MultiCord")
    
    await ctx.send(embed=embed)

@bot.command(name='shutdown', hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    """Shutdown the bot (owner only)."""
    await ctx.send("Shutting down...")
    await bot.close()

if __name__ == "__main__":
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)
    
    # Run the bot
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        logger.error("Invalid bot token! Please check your config.toml")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        sys.exit(1)