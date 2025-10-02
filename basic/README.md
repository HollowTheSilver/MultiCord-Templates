# Basic Discord Bot

A simple, extensible Discord bot template for MultiCord. Perfect for beginners and quick bot deployments.

## Features

- Command handling with customizable prefix
- Event processing (guild join/leave, errors)
- Built-in commands: ping, uptime, stats, info
- Configurable logging
- Clean error handling
- MultiCord integration ready

## Quick Start

### Prerequisites

- Python 3.9 or higher
- A Discord bot token ([Get one here](https://discord.com/developers/applications))
- MultiCord CLI installed

### Installation

1. Create a new bot using this template:
   ```bash
   multicord bot create my-bot --template basic
   ```

2. Configure your bot token:
   ```bash
   cd bots/my-bot
   # Edit config.toml and add your bot token
   ```

3. Start the bot:
   ```bash
   multicord bot start my-bot
   ```

## Configuration

Edit `config.toml` to customize your bot:

```toml
[bot]
token = "YOUR_BOT_TOKEN_HERE"
prefix = "!"
description = "A basic Discord bot powered by MultiCord"

[logging]
level = "INFO"
```

## Available Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `!ping` | Check bot latency | `!ping` |
| `!uptime` | Show how long the bot has been running | `!uptime` |
| `!stats` | Display bot statistics (servers, users, etc.) | `!stats` |
| `!info` | Show bot information | `!info` |
| `!shutdown` | Shutdown the bot (owner only) | `!shutdown` |

## Required Discord Permissions

- **Send Messages** - To respond to commands
- **Embed Links** - To send rich embeds
- **Read Message History** - To process messages

## Extending the Bot

### Adding Commands

Add new commands to `bot.py`:

```python
@bot.command(name="hello")
async def hello(ctx):
    """Say hello to the user."""
    await ctx.send(f"Hello {ctx.author.mention}!")
```

### Creating Cogs

For better organization, create cogs in a `cogs/` directory:

```python
# cogs/greetings.py
from discord.ext import commands

class Greetings(commands.Cog):
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello!")

async def setup(bot):
    await bot.add_cog(Greetings(bot))
```

## Troubleshooting

### Bot doesn't start

- Check that your token is correct in `config.toml`
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check logs in `logs/bot.log` for errors

### Commands don't work

- Verify the bot has "Read Messages" and "Send Messages" permissions
- Check that message content intent is enabled in Discord Developer Portal
- Ensure you're using the correct prefix

## License

MIT License - see root repository LICENSE file

---

**Made with [MultiCord](https://github.com/HollowTheSilver/MultiCord)** | [Report Issues](https://github.com/HollowTheSilver/MultiCord-Templates/issues)
