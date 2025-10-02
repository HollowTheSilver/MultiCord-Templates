# MultiCord Discord Bot Templates

**Official template repository for [MultiCord](https://github.com/HollowTheSilver/MultiCord) - Professional Discord bot management made easy.**

This repository contains production-ready Discord bot templates that work seamlessly with the MultiCord CLI. Templates are automatically downloaded when you install MultiCord, and you can also create custom template repositories for your own bot architectures.

## 🚀 Available Templates

### Basic Bot Template
**Perfect for**: Learning Discord.py, simple utility bots, bot foundations

A minimal yet complete Discord bot with:
- Command handling with prefix and slash commands
- Event processing (on_ready, on_message, on_member_join)
- Structured logging to files and console
- Configuration management with TOML
- Error handling and graceful shutdown
- Health check endpoints

**Use case**: Start here for any new bot project or to learn Discord.py fundamentals.

### Moderation Bot Template
**Perfect for**: Community management, server moderation, anti-spam

A comprehensive moderation bot with:
- Kick, ban, timeout, and warn systems
- Warning tracking and history
- Role management (add/remove roles)
- Message purge functionality
- Moderation logging with embeds
- Permission checks for all commands

**Use case**: Server moderation, community management, maintaining order in large servers.

### Music Bot Template
**Perfect for**: Playing music, voice channel utilities, entertainment

A feature-rich music bot with:
- YouTube integration (youtube-dl/yt-dlp)
- Queue management (add, skip, remove, clear)
- Playback controls (pause, resume, stop, volume)
- Now playing display with embeds
- Voice channel management
- Error handling for connection issues

**Use case**: Add music functionality to your server, create a dedicated music bot.

## 📦 Installation & Usage

### Automatic Installation (Recommended)
Templates are automatically downloaded when you run MultiCord for the first time:

```bash
# Install MultiCord CLI
pip install multicord

# Templates are downloaded on first use
multicord bot create my-bot --template basic
```

### Manual Template Repository Management

```bash
# List available templates
multicord template list

# Update templates to latest version
multicord template update

# Add a custom template repository
multicord template add https://github.com/yourname/custom-templates.git

# Get detailed information about a template
multicord template info moderation
```

## 🛠️ Creating a Bot from a Template

```bash
# Create a new bot from the basic template
multicord bot create my-awesome-bot --template basic

# Create a moderation bot
multicord bot create mod-bot --template moderation

# Create a music bot
multicord bot create music-bot --template music
```

After creation, configure your bot:
1. Edit `config.toml` with your bot token and settings
2. Install dependencies: `pip install -r requirements.txt`
3. Start your bot: `multicord bot start my-awesome-bot`

## 📝 Template Structure

Each template follows a standard structure:

```
template-name/
├── bot.py              # Main bot file (required)
├── config.toml         # Configuration file (required)
├── requirements.txt    # Python dependencies (required)
└── README.md          # Template documentation (required)
```

### Required Files

**bot.py**
- Entry point for the Discord bot
- Must handle configuration loading from config.toml
- Should implement graceful shutdown
- Must include proper error handling

**config.toml**
- Bot configuration (token, prefix, etc.)
- Template metadata
- Should use clear section names

**requirements.txt**
- Python package dependencies
- Pin discord.py version
- Include all necessary libraries

**README.md**
- Template description and features
- Configuration instructions
- Usage examples
- Required Discord permissions

## 🤝 Contributing

We welcome community contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Creating new templates
- Template naming conventions
- Testing requirements
- Pull request process

### Quick Start for Contributors

1. Fork this repository
2. Create a new directory for your template
3. Follow the template structure above
4. Add your template to `manifest.json`
5. Test with MultiCord CLI
6. Submit a pull request

## 📋 Template Requirements

All templates must:
- ✅ Use Discord.py 2.0+
- ✅ Support Python 3.9+
- ✅ Include all four required files
- ✅ Have clear configuration options
- ✅ Include error handling
- ✅ Follow Discord.py best practices
- ✅ Be well-documented
- ✅ Not include bot tokens or secrets

## 🏷️ Template Categories

Templates are organized by category:
- **General**: Basic bots, utility bots, starter templates
- **Moderation**: Community management, anti-spam, logging
- **Entertainment**: Music, games, fun commands
- **Utility**: Tools, automation, integration bots
- **Advanced**: Complex architectures, multi-service bots

## 📜 License

All templates in this repository are released under the MIT License. See [LICENSE](LICENSE) for details.

You are free to:
- Use templates for commercial projects
- Modify templates for your needs
- Distribute modified versions
- Include templates in your own projects

## 🔗 Related Projects

- **[MultiCord CLI](https://github.com/HollowTheSilver/MultiCord)** - Official Discord bot management tool
- **[Discord.py](https://github.com/Rapptz/discord.py)** - Python Discord API wrapper
- **[Discord Developer Portal](https://discord.com/developers)** - Create and manage Discord applications

## 📚 Resources

- **[Discord.py Documentation](https://discordpy.readthedocs.io/)**
- **[Discord Developer Docs](https://discord.com/developers/docs)**
- **[MultiCord Documentation](https://docs.multicord.io)** (coming soon)
- **[Discord.py Community](https://discord.gg/dpy)**

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/HollowTheSilver/MultiCord-Templates/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HollowTheSilver/MultiCord-Templates/discussions)
- **Discord**: Join the MultiCord community server (coming soon)

## 🌟 Featured Community Templates

Want your custom template repository featured here? Submit a PR with your repository link and description!

---

**Made with ❤️ by the MultiCord Team**

Star this repository if you find these templates useful!