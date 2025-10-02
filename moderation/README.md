# Moderation Discord Bot

A comprehensive moderation bot template for MultiCord. Includes kick, ban, timeout, warning system, and role management.

## Features

- **Moderation Commands**: kick, ban, unban, timeout, warn
- **Role Management**: add/remove roles, create/delete roles
- **Warning System**: track user warnings with automatic actions
- **Audit Logging**: detailed logs of all moderation actions
- **Configurable Actions**: set thresholds for automatic moderation
- **MultiCord Integration**: ready for multi-bot orchestration

## Quick Start

### Prerequisites

- Python 3.9 or higher
- A Discord bot token with moderation permissions
- MultiCord CLI installed

### Installation

1. Create a new bot using this template:
   ```bash
   multicord bot create my-moderator --template moderation
   ```

2. Configure your bot:
   ```bash
   cd bots/my-moderator
   # Edit config.toml and add your bot token
   ```

3. Start the bot:
   ```bash
   multicord bot start my-moderator
   ```

## Configuration

Edit `config.toml` to customize moderation settings:

```toml
[bot]
token = "YOUR_BOT_TOKEN_HERE"
prefix = "!"
description = "A moderation bot powered by MultiCord"

[moderation]
log_channel_id = 1234567890  # Channel for mod logs
auto_timeout_warnings = 3     # Warnings before auto-timeout
auto_ban_warnings = 5         # Warnings before auto-ban
```

## Moderation Commands

### Basic Moderation

| Command | Description | Usage | Permissions |
|---------|-------------|-------|-------------|
| `!kick <member> [reason]` | Kick a member from the server | `!kick @user Spamming` | Kick Members |
| `!ban <member> [reason]` | Ban a member from the server | `!ban @user Rule violation` | Ban Members |
| `!unban <user_id>` | Unban a user by ID | `!unban 123456789` | Ban Members |
| `!timeout <member> <duration> [reason]` | Timeout a member | `!timeout @user 10m Spam` | Moderate Members |
| `!warn <member> <reason>` | Warn a member | `!warn @user Breaking rules` | Moderate Members |
| `!warnings <member>` | View member warnings | `!warnings @user` | Moderate Members |
| `!clearwarns <member>` | Clear member warnings | `!clearwarns @user` | Administrator |

### Role Management

| Command | Description | Usage | Permissions |
|---------|-------------|-------|-------------|
| `!addrole <member> <role>` | Add a role to a member | `!addrole @user Moderator` | Manage Roles |
| `!removerole <member> <role>` | Remove a role from a member | `!removerole @user Muted` | Manage Roles |
| `!createrole <name> [color]` | Create a new role | `!createrole VIP #FFD700` | Manage Roles |
| `!deleterole <role>` | Delete a role | `!deleterole @OldRole` | Manage Roles |

### Utility

| Command | Description | Usage | Permissions |
|---------|-------------|-------|-------------|
| `!purge <amount>` | Delete messages in bulk | `!purge 50` | Manage Messages |
| `!userinfo <member>` | Get user information | `!userinfo @user` | None |
| `!serverinfo` | Get server information | `!serverinfo` | None |

## Required Discord Permissions

### Essential Permissions
- **Kick Members** - To kick users
- **Ban Members** - To ban/unban users
- **Moderate Members** - To timeout users
- **Manage Roles** - To add/remove/create roles
- **Manage Messages** - To purge messages

### Optional Permissions
- **View Audit Log** - To track who performed actions
- **Manage Channels** - For advanced moderation features

## Warning System

The bot includes a sophisticated warning system:

1. **Issue Warning**: `!warn @user Reason here`
2. **Automatic Actions**:
   - 3 warnings → 10-minute timeout
   - 5 warnings → Automatic ban
3. **View Warnings**: `!warnings @user`
4. **Clear Warnings**: `!clearwarns @user` (Admin only)

Configure thresholds in `config.toml`:
```toml
[moderation]
auto_timeout_warnings = 3
auto_ban_warnings = 5
```

## Audit Logging

All moderation actions are logged to a designated channel:

1. Create a `#mod-logs` channel in your server
2. Get the channel ID (Enable Developer Mode → Right-click channel → Copy ID)
3. Add to `config.toml`:
   ```toml
   [moderation]
   log_channel_id = YOUR_CHANNEL_ID
   ```

Logged events include:
- Kicks, bans, unbans
- Timeouts and warnings
- Role changes
- Message purges

## Customization

### Adjusting Timeout Durations

Edit the timeout command in `bot.py`:

```python
# Supported formats: 10s, 5m, 1h, 2d
duration_map = {
    's': 1,           # seconds
    'm': 60,          # minutes
    'h': 3600,        # hours
    'd': 86400        # days
}
```

### Adding Custom Actions

Add new moderation commands:

```python
@bot.command(name='slowmode')
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    """Set slowmode for the current channel."""
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Slowmode set to {seconds} seconds")
```

## Troubleshooting

### Permission Errors

- Ensure the bot role is **above** the roles it needs to manage
- Verify all required permissions are enabled in Discord Developer Portal
- Check that the bot has permissions in the specific channels

### Warnings Not Working

- Ensure the bot can write to files (check logs directory permissions)
- Verify warning thresholds are set correctly in config.toml

### Audit Logs Not Appearing

- Confirm `log_channel_id` is correct in config.toml
- Ensure the bot has "Send Messages" and "Embed Links" permissions in that channel

## Security Considerations

- **Role Hierarchy**: Bot can only moderate users below its highest role
- **Permission Checks**: All commands verify user permissions
- **Audit Trail**: All actions are logged for accountability
- **Owner Protection**: Bot owner cannot be moderated

## License

MIT License - see root repository LICENSE file

---

**Made with [MultiCord](https://github.com/HollowTheSilver/MultiCord)** | [Report Issues](https://github.com/HollowTheSilver/MultiCord-Templates/issues)
