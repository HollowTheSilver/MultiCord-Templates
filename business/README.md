# Professional Business Discord Bot

A production-ready Discord bot template designed for commissioned projects and professional deployments. Features automatic cog loading, structured logging, TOML-based configuration, and enterprise-grade error handling.

## ✨ Features

- **🔌 Automatic Cog Loading** - Drop cog folders into `cogs/` and they load automatically
- **📝 Structured Logging** - Professional logging to both console and file
- **⚙️ TOML Configuration** - Clean, readable configuration management
- **🔒 Environment Variables** - Secure token and secret management
- **🛡️ Error Handling** - Comprehensive global error handling for all commands
- **🎯 Modular Design** - Easy to extend with new features via cogs
- **🚀 Production Ready** - Built with best practices for commissioned work

## 📋 Prerequisites

- Python 3.9 or higher
- A Discord bot token ([Get one here](https://discord.com/developers/applications))
- Basic familiarity with Discord bots

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Your Bot

**Option A: Using Environment Variables (Recommended for production)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your bot token
DISCORD_TOKEN=your_actual_token_here
```

**Option B: Using .env File for Development**

The bot automatically reads from `.env` if it exists.

### 3. Customize Configuration

Edit `config.toml` to customize your bot:

```toml
[bot]
name = "Your Bot Name"
prefix = "!"  # Change command prefix
status = "Type !help"  # Bot status message

[bot.privileged_intents]
message_content = true  # Enable if you need to read messages
members = false         # Enable if you need member events
```

### 4. Run Your Bot

```bash
python bot.py
```

You should see:
```
[2025-01-20 12:00:00] [INFO] discord: Starting bot setup...
[2025-01-20 12:00:00] [INFO] discord: No cogs directory found - running without extensions
[2025-01-20 12:00:00] [INFO] discord: Bot setup complete
[2025-01-20 12:00:00] [INFO] discord: Bot is ready!
[2025-01-20 12:00:00] [INFO] discord:   Logged in as: YourBot#1234 (ID: 123456789)
```

## 📦 Adding Features with Cogs

This bot uses Discord.py's cog system for modular features. Adding functionality is as simple as dropping a cog folder into the `cogs/` directory.

### Using MultiCord CLI (Recommended)

If you created this bot with MultiCord CLI, you can install cogs easily:

```bash
# List available cogs
multicord cog available

# Install a cog (e.g., custom permissions system)
multicord cog add your-bot-name permissions

# List installed cogs
multicord cog list your-bot-name

# Update all cogs
multicord cog update your-bot-name --all
```

### Manual Cog Installation

1. Create a folder in `cogs/` (e.g., `cogs/mycog/`)
2. Add `__init__.py` with your cog class
3. Restart the bot - it will automatically load!

**Example Cog Structure:**
```
cogs/
└── mycog/
    ├── __init__.py      # Cog entry point with setup() function
    ├── commands.py      # Your command implementations (optional)
    └── requirements.txt # Additional dependencies (optional)
```

**Minimal Cog Example (`cogs/mycog/__init__.py`):**
```python
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello from my cog!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

## 🔧 Configuration Reference

### Bot Settings (`config.toml`)

| Setting | Description | Default |
|---------|-------------|---------|
| `bot.name` | Bot display name | "Business Bot" |
| `bot.prefix` | Command prefix | "!" |
| `bot.enable_help` | Enable built-in help command | true |
| `bot.status` | Bot status in Discord | "Ready to serve" |

### Privileged Intents

Some features require privileged intents to be enabled in the [Discord Developer Portal](https://discord.com/developers/applications):

| Intent | Required For | Enable in Portal |
|--------|--------------|------------------|
| `message_content` | Reading message content | ✅ Required for most bots |
| `members` | Member join/leave events | Only if needed |
| `presences` | User status updates | Rarely needed |

**How to enable:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. Navigate to **Bot** section
4. Scroll to **Privileged Gateway Intents**
5. Toggle the required intents
6. Update `config.toml` to match

## 📁 Project Structure

```
your-bot/
├── bot.py              # Main bot application
├── config.toml         # Bot configuration
├── .env                # Environment variables (create from .env.example)
├── .env.example        # Environment template
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── logs/               # Log files (auto-created)
│   └── bot.log
└── cogs/               # Bot extensions (auto-loaded)
    ├── .gitkeep
    └── permissions/    # Example: custom permissions cog
        ├── __init__.py
        └── ...
```

## 🐛 Troubleshooting

### Bot Won't Start

**Error: `No Discord token found`**
```bash
# Solution: Set your token in .env file
echo "DISCORD_TOKEN=your_token_here" > .env
```

**Error: `Privileged intent provided is not enabled`**
```bash
# Solution: Enable the intent in Discord Developer Portal
# Then update config.toml:
[bot.privileged_intents]
message_content = true  # Set to true if you enabled it
```

### Cog Won't Load

**Error: `Skipping mycog - not a valid Python package`**
```bash
# Solution: Ensure your cog has __init__.py
touch cogs/mycog/__init__.py
```

**Error: `Failed to load cog mycog: Extension must have a setup function`**
```python
# Solution: Add setup() function to your cog's __init__.py
async def setup(bot):
    await bot.add_cog(YourCog(bot))
```

### Bot Crashes on Command

Check the log files in `logs/bot.log` for detailed error messages. The bot includes comprehensive error handling, so most errors will be caught and logged.

## 🔒 Security Best Practices

1. **Never commit `.env` or `config.toml` with secrets** - Add them to `.gitignore`
2. **Use environment variables for production** - Don't hardcode tokens
3. **Regenerate tokens if exposed** - If you accidentally commit a token, regenerate it immediately
4. **Limit bot permissions** - Only request permissions your bot actually needs
5. **Keep dependencies updated** - Run `pip install --upgrade -r requirements.txt` regularly

## 📝 Logging

Logs are written to two locations:

- **Console**: Real-time colored output for development
- **File**: `logs/bot.log` for persistent logging and debugging

Log levels can be configured in `config.toml`:
```toml
[logging]
level = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## 🚀 Deploying to Production

### Local Hosting

```bash
# Use a process manager like systemd or supervisor
# Example systemd service:
[Unit]
Description=Discord Business Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/path/to/bot
ExecStart=/path/to/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Cloud Hosting

This bot works great with:
- **Heroku** - Add `Procfile`: `worker: python bot.py`
- **Railway** - Automatically detects Python and requirements.txt
- **AWS/GCP/Azure** - Use container or VM hosting
- **DigitalOcean** - App Platform or Droplets

### Using MultiCord API (Coming Soon)

The MultiCord platform will offer managed cloud hosting:
```bash
multicord bot deploy your-bot-name --cloud
```

## 🆘 Support

- **MultiCord Issues**: [GitHub Issues](https://github.com/HollowTheSilver/MultiCord/issues)
- **Discord.py Docs**: [discord.py Documentation](https://discordpy.readthedocs.io/)
- **Discord Developers**: [Discord Developer Portal](https://discord.com/developers/docs)

## 📜 License

This template is part of the MultiCord project. Use it freely for your commissioned projects and commercial work.

---

**Built with ❤️ using MultiCord** - Making Discord bot development professional and efficient.
