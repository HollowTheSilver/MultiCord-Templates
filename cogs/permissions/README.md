# Custom Permissions System

**Enterprise-grade hierarchical permission system for Discord bots with intelligent role detection.**

> **Author**: HollowTheSilver
> **Version**: 1.0.0
> **License**: MIT
> **Discord.py**: >= 2.0.0

---

## 🌟 Features

### 🎯 Core Capabilities
- **9-Level Permission Hierarchy** - From `BANNED` (-1) to `BOT_OWNER` (200)
- **Intelligent Role Auto-Detection** - Automatically classifies and configures roles
- **Unicode Text Normalization** - Handles fancy Discord names with special characters
- **Guild-Specific Overrides** - Customize permissions per server
- **Audit Logging** - Complete trail of permission changes for compliance
- **Optional Database Persistence** - SQLite support with in-memory fallback

### 🧠 Intelligent Features
- **Role Classification** - Distinguishes between Authority, Bot, Integration, Cosmetic, Functional, and Temporary roles
- **Multi-Factor Owner Detection** - Smart identification of server owner roles
- **Channel Permission Analysis** - Detects functional vs authority roles
- **Performance Optimized** - Limits analysis to avoid ticket system traps

### 🎨 Developer-Friendly
- **Easy Decorators** - `@require_permission()`, `@require_level()`, `@channel_only()`
- **Flexible Configuration** - Works with or without database
- **Clean API** - Well-documented methods and clear interfaces
- **Battle-Tested** - Used in production commissioned bots

---

## 📦 Installation

### Via MultiCord CLI (Recommended)
```bash
# Install into existing bot
multicord cog add my-bot permissions
```

### Manual Installation
```bash
# 1. Copy the permissions directory to your bot's cogs folder
cp -r permissions /path/to/your/bot/cogs/

# 2. Install dependencies
pip install -r cogs/permissions/requirements.txt

# 3. Load the cog in your bot
# Add to your bot's main file:
await bot.load_extension('cogs.permissions')
```

### Dependencies
- `discord.py >= 2.0.0` - Discord API wrapper
- `unidecode >= 1.3.0` - Unicode text normalization
- `aiosqlite >= 0.17.0` - Optional database support

---

## 🚀 Quick Start

### Basic Usage (In-Memory)
```python
# bot.py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Load permissions cog
await bot.load_extension('cogs.permissions')

# That's it! Permissions system is now active
```

### With Database Persistence
```python
# bot.py
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Configure permissions with database
bot.config = {
    'permissions': {
        'use_database': True,
        'db_path': 'data/permissions.db'
    }
}

# Load permissions cog
await bot.load_extension('cogs.permissions')
```

### Using Permission Decorators
```python
from discord.ext import commands
from cogs.permissions.permission_models import PermissionLevel

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.permissions = bot.get_cog('Permissions').permissions

    @commands.command()
    @commands.check(lambda ctx: ctx.cog.permissions.has_permission(
        ctx.author,
        "moderation.kick",
        ctx.guild
    ))
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kick a member from the server."""
        await member.kick(reason=reason)
        await ctx.send(f"✅ Kicked {member.mention}")

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """Ban a member (requires ADMIN level)."""
        # Check permission level
        user_level = await self.permissions.get_user_permission_level(
            ctx.author,
            ctx.guild
        )

        if user_level < PermissionLevel.ADMIN:
            await ctx.send("❌ You need ADMIN level to ban members")
            return

        await member.ban(reason=reason)
        await ctx.send(f"✅ Banned {member.mention}")
```

---

## 🎓 Permission Hierarchy

### Permission Levels
```
BOT_OWNER (200)     - Bot owner (highest authority)
    ↓
BOT_ADMIN (150)     - Bot administrators (cross-server)
    ↓
OWNER (100)         - Server owner / top administrators
    ↓
LEAD_ADMIN (90)     - Senior administrators
    ↓
ADMIN (80)          - Basic administrators
    ↓
LEAD_MOD (65)       - Senior/Lead moderators
    ↓
MODERATOR (50)      - Basic moderators
    ↓
MEMBER (10)         - Trusted members, VIPs
    ↓
EVERYONE (0)        - Default level (all members)
    ↓
BANNED (-1)         - Explicitly banned from commands
```

### Auto-Detection Logic

The system automatically analyzes role names and Discord permissions to suggest appropriate levels:

**Name Pattern Matching**:
- "owner", "founder" → `OWNER` (100)
- "admin", "administrator" → `ADMIN` (80)
- "mod", "moderator" → `MODERATOR` (50)
- "member", "verified", "vip" → `MEMBER` (10)

**Discord Permission Analysis**:
- Has `administrator` → `ADMIN` minimum
- Has `manage_guild` → `LEAD_ADMIN` minimum
- Has `kick_members` or `ban_members` → `MODERATOR` minimum

**Position-Based Fallback**:
- Top 10% of roles → Higher admin levels
- Middle roles → Moderation levels
- Lower roles → Member/Everyone levels

---

## 🎮 Discord Commands

### Auto-Configuration
```
/permissions auto-configure
```
Automatically detects and configures all roles in the server.

**What it does**:
- Classifies each role (Authority, Bot, Cosmetic, etc.)
- Suggests permission levels based on names and Discord permissions
- Applies configurations server-wide
- Generates detailed report

**Example Output**:
```
🔧 Auto-Configuration Complete!

✅ Configured 12 Authority Roles:
  • Server Owner → OWNER (100)
  • Administrator → ADMIN (80)
  • Moderator → MODERATOR (50)
  • Trusted Member → MEMBER (10)

ℹ️ Skipped 8 roles:
  • Bot roles: 3
  • Cosmetic roles: 4
  • Integration roles: 1

Run /permissions list-roles to see full configuration.
```

### Role Management
```
/permissions set-role @Moderator MODERATOR
/permissions set-role @Helper MEMBER
/permissions remove-role @OldRole
/permissions list-roles
```

### Command Permission Overrides
```
/permissions set-command ban ADMIN
/permissions set-command warn MODERATOR
/permissions list-commands
```

### User-Specific Overrides
```
/permissions grant-user @User moderation.kick
/permissions deny-user @BadActor commands.all
/permissions remove-user @User moderation.kick
```

### Information & Auditing
```
/permissions check @User
/permissions audit [limit]
/permissions info
```

---

## 🏗️ Architecture

### File Structure
```
permissions/
├── __init__.py                # Cog entry point
├── permissions.py             # Main permission manager (1900+ lines)
├── permission_models.py       # Data models and enums
├── permission_persistence.py  # Database layer (optional)
├── embeds.py                  # Discord embed utilities
├── requirements.txt           # Dependencies
├── manifest.json              # Metadata for CLI
└── README.md                  # This file
```

### Key Components

**PermissionManager** - Core permission logic
- Role classification and auto-detection
- Permission checking and validation
- Guild configuration management

**RoleClassifier** - Intelligent role analysis
- Unicode text normalization
- Multi-factor classification
- Performance optimizations

**PermissionPersistence** - Data storage
- SQLite database support
- In-memory fallback
- Async operations

---

## 📝 Configuration

### In-Memory Mode (Default)
No configuration needed. All data stored in memory and lost on restart.

### Database Mode
```python
# bot.py or config.toml
bot.config = {
    'permissions': {
        'use_database': True,
        'db_path': 'data/permissions.db'  # Path to SQLite file
    }
}
```

**Benefits of Database Mode**:
- Persistent role configurations
- Audit log retention
- Permission history
- Faster startup (cached data)

---

## 🔧 Advanced Usage

### Custom Permission Nodes
```python
# Define custom permissions
permissions.register_node(
    name="economy.admin",
    default_level=PermissionLevel.ADMIN,
    description="Manage economy system"
)

permissions.register_node(
    name="tickets.create",
    default_level=PermissionLevel.MEMBER,
    description="Create support tickets"
)

# Check custom permissions
if await permissions.has_permission(user, "economy.admin", guild):
    # User can manage economy
    pass
```

### Permission Scopes
```python
from cogs.permissions.permission_models import PermissionScope, PermissionOverride

# Grant permission only in specific channel
override = PermissionOverride(
    target_type="user",
    target_id=user.id,
    permission_node="moderation.kick",
    granted=True,
    scope_type=PermissionScope.CHANNEL,
    scope_id=channel.id,
    reason="Moderator in this channel only"
)

await permissions.add_override(override)
```

### Temporary Permissions
```python
from datetime import datetime, timedelta

# Grant temporary permission
override = PermissionOverride(
    target_type="user",
    target_id=user.id,
    permission_node="moderation.warn",
    granted=True,
    scope_type=PermissionScope.GUILD,
    scope_id=guild.id,
    expires_at=datetime.utcnow() + timedelta(hours=24),
    reason="Temporary moderator for event"
)

await permissions.add_override(override)
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Roles not auto-configuring correctly
- **Solution**: Ensure role names follow common patterns (owner, admin, mod)
- **Alternative**: Manually set roles with `/permissions set-role`

**Issue**: Database permissions not persisting
- **Solution**: Check `db_path` is writable and `use_database` is `True`
- **Check**: Look for `permissions.db` file creation

**Issue**: Permission checks always failing
- **Solution**: Run `/permissions auto-configure` first
- **Check**: Verify with `/permissions check @YourUser`

**Issue**: ImportError for unidecode
- **Solution**: Install dependencies: `pip install -r requirements.txt`

### Debug Mode
```python
# Enable detailed logging
import logging

logging.getLogger('permissions').setLevel(logging.DEBUG)
```

---

## 📚 API Reference

### Core Methods

```python
# Check if user has permission
has_perm = await permissions.has_permission(
    user: discord.User,
    node: str,
    guild: discord.Guild
) -> bool

# Get user's permission level
level = await permissions.get_user_permission_level(
    user: discord.User,
    guild: discord.Guild
) -> PermissionLevel

# Register custom permission node
permissions.register_node(
    name: str,
    default_level: PermissionLevel,
    description: str
)

# Set role permission level
await permissions.set_role_level(
    guild: discord.Guild,
    role: discord.Role,
    level: PermissionLevel
)

# Auto-configure all roles
results = await permissions.auto_configure_guild(
    guild: discord.Guild
)
```

---

## 🤝 Contributing

This cog is part of the MultiCord Templates repository. Contributions welcome!

### Reporting Issues
- **GitHub Issues**: https://github.com/HollowTheSilver/MultiCord-Templates/issues
- **Include**: Bot version, error messages, steps to reproduce

### Submitting Improvements
1. Fork the MultiCord-Templates repository
2. Create a feature branch
3. Make your changes to `cogs/permissions/`
4. Test thoroughly
5. Submit pull request with clear description

---

## 📄 License

MIT License - See repository LICENSE file for details.

You are free to use this cog in commercial and personal projects.

---

## 🙏 Credits

**Author**: HollowTheSilver
**Project**: MultiCord
**Repository**: https://github.com/HollowTheSilver/MultiCord-Templates

Built with:
- Discord.py by Rapptz
- unidecode library
- Lots of caffeine and commissioned bot projects

---

## 📖 Additional Documentation

- **EXAMPLES.md** - Real-world usage examples
- **API.md** - Complete API reference
- **CHANGELOG.md** - Version history

---

**Questions? Issues? Ideas?**
Open an issue on GitHub or join the MultiCord community server!

**Made with ❤️ for professional Discord bot development**
