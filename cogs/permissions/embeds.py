"""
Embed Utilities for Permissions System
======================================

Standard embed creation utilities for consistent messaging.
"""

import discord
from datetime import datetime
from typing import Optional


def create_base_embed(
    title: str,
    description: str,
    color: discord.Color,
    user: Optional[discord.User] = None
) -> discord.Embed:
    """Create a base embed with consistent formatting."""
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.utcnow()
    )

    if user:
        embed.set_footer(
            text=f"Requested by {user.display_name}",
            icon_url=user.display_avatar.url if user.display_avatar else None
        )

    return embed


def create_error_embed(
    title: str,
    description: str,
    user: Optional[discord.User] = None
) -> discord.Embed:
    """Create an error embed (red)."""
    return create_base_embed(title, description, discord.Color.red(), user)


def create_success_embed(
    title: str,
    description: str,
    user: Optional[discord.User] = None
) -> discord.Embed:
    """Create a success embed (green)."""
    return create_base_embed(title, description, discord.Color.green(), user)


def create_warning_embed(
    title: str,
    description: str,
    user: Optional[discord.User] = None
) -> discord.Embed:
    """Create a warning embed (yellow/gold)."""
    return create_base_embed(title, description, discord.Color.gold(), user)


def create_info_embed(
    title: str,
    description: str,
    user: Optional[discord.User] = None
) -> discord.Embed:
    """Create an info embed (blue)."""
    return create_base_embed(title, description, discord.Color.blue(), user)
