# Contributing to MultiCord Templates

Thank you for your interest in contributing to the MultiCord Templates repository! This document provides guidelines and instructions for creating and submitting Discord bot templates.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Template Requirements](#template-requirements)
- [Creating a New Template](#creating-a-new-template)
- [Template Structure](#template-structure)
- [Testing Your Template](#testing-your-template)
- [Submission Process](#submission-process)
- [Code Standards](#code-standards)
- [Review Process](#review-process)

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:
- Python 3.9 or higher installed
- Discord.py 2.0+ knowledge
- MultiCord CLI installed (`pip install multicord`)
- A Discord bot application (for testing)
- Git installed and configured

### Fork and Clone

1. Fork this repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/MultiCord-Templates.git
   cd MultiCord-Templates
   ```
3. Create a new branch for your template:
   ```bash
   git checkout -b template/your-template-name
   ```

## 📝 Template Requirements

### Mandatory Requirements

All templates **MUST** include:

1. **bot.py** - Main bot file
   - Clear structure and organization
   - Proper error handling
   - Configuration loading from config.toml
   - Graceful shutdown handling
   - Logging implementation

2. **config.toml** - Configuration file
   - Template metadata section
   - Bot configuration section
   - Clear documentation via comments
   - No hardcoded tokens or secrets

3. **requirements.txt** - Dependencies
   - Pinned Discord.py version (>=2.0.0)
   - All necessary dependencies listed
   - Minimal dependencies preferred

4. **README.md** - Documentation
   - Template description
   - Features list
   - Configuration instructions
   - Usage examples
   - Required Discord permissions
   - Screenshots (optional but recommended)

### Optional but Recommended

- **LICENSE** - If different from repository license
- **examples/** - Example usage or command demonstrations
- **.env.example** - Example environment variables
- **tests/** - Unit tests for bot functionality

## 🏗️ Creating a New Template

### Step 1: Choose a Template Name

- Use lowercase with hyphens: `my-template-name`
- Be descriptive but concise
- Avoid generic names like "bot" or "discord-bot"
- Check existing templates to avoid duplicates

### Step 2: Create Directory Structure

```bash
mkdir your-template-name
cd your-template-name
```

### Step 3: Create Required Files

**bot.py Example Structure:**

```python
#!/usr/bin/env python3
"""
[Template Name] - Brief description
A detailed description of what this template does.
"""

import os
import sys
import logging
from pathlib import Path
import discord
from discord.ext import commands
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

# Bot setup
intents = discord.Intents.default()
intents.message_content = True  # Required for message commands

bot = commands.Bot(
    command_prefix=config['bot']['prefix'],
    intents=intents,
    description=config['bot']['description']
)

@bot.event
async def on_ready():
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')

@bot.event
async def on_command_error(ctx, error):
    """Global error handler."""
    if isinstance(error, commands.CommandNotFound):
        return
    logger.error(f'Error in command {ctx.command}: {error}')
    await ctx.send(f'An error occurred: {error}')

# Your commands here
@bot.command(name='hello')
async def hello(ctx):
    """Say hello!"""
    await ctx.send(f'Hello {ctx.author.mention}!')

if __name__ == '__main__':
    try:
        logger.info("Starting bot...")
        bot.run(config['bot']['token'])
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
```

**config.toml Example:**

```toml
[template]
name = "your-template-name"
version = "1.0.0"
description = "Brief description of your template"
author = "Your Name"
discord_py_version = ">=2.0.0"
python_version = ">=3.9"
category = "general"  # general, moderation, entertainment, utility, advanced
tags = ["keyword1", "keyword2", "keyword3"]

[bot]
token = "YOUR_BOT_TOKEN_HERE"  # Users will replace this
prefix = "!"
description = "A cool Discord bot"
activity_type = "playing"  # playing, watching, listening
activity_name = "with commands"

[features]
# Document your template's features
slash_commands = false
prefix_commands = true
database = false  # Does this template use a database?
api_integration = false  # Does this integrate with external APIs?

[permissions]
# Required Discord permissions (as integers or names)
# See: https://discord.com/developers/docs/topics/permissions
required = ["send_messages", "embed_links"]
```

**requirements.txt Example:**

```txt
discord.py>=2.0.0
python-dotenv>=1.0.0
toml>=0.10.0
# Add any other dependencies your bot needs
```

**README.md Template:**

````markdown
# [Template Name]

Brief one-line description of the template.

## Description

Detailed description of what this template does and what makes it useful.

## Features

- Feature 1
- Feature 2
- Feature 3

## Prerequisites

- Python 3.9 or higher
- A Discord bot token
- [Any other requirements]

## Configuration

1. Edit `config.toml`:
   ```toml
   [bot]
   token = "your-bot-token-here"
   prefix = "!"
   ```

2. [Additional configuration steps]

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python bot.py
```

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `!command` | Does something | `!command [arg]` |

## Required Discord Permissions

- Permission 1
- Permission 2

## Screenshots

[Optional: Add screenshots of your bot in action]

## Notes

[Any additional notes or warnings]

## License

[If different from repository license]
````

## 🧪 Testing Your Template

### Local Testing

1. **Create a test bot**:
   ```bash
   multicord bot create test-bot --template your-template-name
   ```

2. **Configure the bot**:
   - Add your bot token to config.toml
   - Adjust any other settings

3. **Run the bot**:
   ```bash
   multicord bot start test-bot
   ```

4. **Test all features**:
   - All commands work as documented
   - Error handling works properly
   - Configuration options work
   - Bot shuts down gracefully

### Validation Checklist

Before submitting, verify:

- [ ] Bot runs without errors
- [ ] All commands work as documented
- [ ] Configuration is clear and well-documented
- [ ] No hardcoded tokens or secrets
- [ ] Logging works properly
- [ ] Error handling is comprehensive
- [ ] Code follows PEP 8 style guidelines
- [ ] All required files are present
- [ ] README.md is complete and accurate
- [ ] requirements.txt includes all dependencies
- [ ] Template works with MultiCord CLI

## 📤 Submission Process

### 1. Update manifest.json

Add your template to `manifest.json`:

```json
{
  "your-template-name": {
    "name": "Your Template Name",
    "description": "Brief description",
    "version": "1.0.0",
    "author": "Your Name",
    "category": "general",
    "tags": ["tag1", "tag2"],
    "discord_py_version": ">=2.0.0",
    "python_version": ">=3.9",
    "files": ["bot.py", "config.toml", "requirements.txt", "README.md"],
    "featured": false
  }
}
```

### 2. Commit Your Changes

```bash
git add your-template-name/
git add manifest.json
git commit -m "Add [template-name] template"
```

### 3. Push to Your Fork

```bash
git push origin template/your-template-name
```

### 4. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Fill in the PR template:
   - Template name and description
   - What problem it solves
   - Any special considerations
   - Screenshots (if applicable)

## 💻 Code Standards

### Python Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small
- Use type hints where appropriate

### Discord.py Best Practices

- Use intents appropriately
- Handle errors gracefully
- Implement proper permission checks
- Use embeds for rich content
- Avoid rate limiting issues

### Security

- **NEVER** commit bot tokens
- **NEVER** commit API keys or secrets
- Use environment variables or config files
- Validate all user input
- Implement proper permission checks

## 👀 Review Process

After submission, maintainers will:

1. **Review your code** for:
   - Functionality
   - Code quality
   - Security issues
   - Documentation completeness

2. **Test the template** with MultiCord CLI

3. **Provide feedback** via PR comments

4. **Request changes** if needed

5. **Merge** once approved

### Review Timeline

- Initial review: Within 3-7 days
- Follow-up reviews: Within 2-3 days
- Merge: Once all feedback is addressed

## 🎯 Template Categories

### General
Basic bots, utility bots, starter templates

### Moderation
Community management, anti-spam, logging, role management

### Entertainment
Music bots, games, fun commands, trivia

### Utility
Tools, automation, integration bots, productivity

### Advanced
Complex architectures, multi-service bots, advanced patterns

## ❓ Questions?

- **Issues**: [GitHub Issues](https://github.com/HollowTheSilver/MultiCord-Templates/issues)
- **Discussions**: [GitHub Discussions](https://github.com/HollowTheSilver/MultiCord-Templates/discussions)
- **Discord**: Join our community server (coming soon)

## 📜 Code of Conduct

Please note that this project has a Code of Conduct. By participating, you agree to abide by its terms.

---

Thank you for contributing to MultiCord Templates! Your work helps the entire Discord bot community. 🎉