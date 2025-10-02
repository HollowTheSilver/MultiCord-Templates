# Music Discord Bot

A feature-rich music bot template for MultiCord with YouTube integration, queue management, and playback controls.

## Features

- **YouTube Playback**: Play songs from YouTube URLs or search queries
- **Queue Management**: Add, remove, skip, and view queued songs
- **Playback Controls**: Play, pause, resume, stop, skip, volume control
- **Now Playing**: Display current song information
- **Auto-disconnect**: Automatically leaves voice channel when queue is empty
- **MultiCord Integration**: Ready for multi-bot orchestration

## Prerequisites

### System Requirements

- Python 3.9 or higher
- **FFmpeg** installed and in system PATH
- A Discord bot token with voice permissions
- MultiCord CLI installed

### Installing FFmpeg

**Windows:**
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

## Quick Start

### Installation

1. Create a new bot using this template:
   ```bash
   multicord bot create my-music-bot --template music
   ```

2. Install dependencies:
   ```bash
   cd bots/my-music-bot
   pip install -r requirements.txt
   ```

3. Configure your bot:
   ```bash
   # Edit config.toml and add your bot token
   ```

4. Start the bot:
   ```bash
   multicord bot start my-music-bot
   ```

## Configuration

Edit `config.toml` to customize your music bot:

```toml
[bot]
token = "YOUR_BOT_TOKEN_HERE"
prefix = "!"
description = "A music bot powered by MultiCord"

[music]
default_volume = 50           # Default volume (0-100)
max_queue_size = 50           # Maximum songs in queue
auto_disconnect_timeout = 300  # Seconds before auto-disconnect (0 = disabled)
```

## Music Commands

### Playback

| Command | Description | Usage | Example |
|---------|-------------|-------|---------|
| `!play <query>` | Play a song from YouTube | `!play <URL or search>` | `!play Never Gonna Give You Up` |
| `!pause` | Pause the current song | `!pause` | - |
| `!resume` | Resume playback | `!resume` | - |
| `!stop` | Stop playback and clear queue | `!stop` | - |
| `!skip` | Skip to the next song | `!skip` | - |
| `!volume <0-100>` | Set playback volume | `!volume <level>` | `!volume 75` |

### Queue Management

| Command | Description | Usage | Example |
|---------|-------------|-------|---------|
| `!queue` | View the current queue | `!queue` | - |
| `!nowplaying` | Show current song info | `!nowplaying` | - |
| `!remove <position>` | Remove a song from queue | `!remove <number>` | `!remove 3` |
| `!clear` | Clear the entire queue | `!clear` | - |

### Voice

| Command | Description | Usage | Example |
|---------|-------------|-------|---------|
| `!join` | Join your voice channel | `!join` | - |
| `!leave` | Leave voice channel | `!leave` | - |

## Required Discord Permissions

### Essential Permissions
- **Send Messages** - To respond to commands
- **Embed Links** - To send rich embeds
- **Connect** - To join voice channels
- **Speak** - To play audio

### Optional Permissions
- **Move Members** - To move users between channels
- **Priority Speaker** - For priority audio

## Usage Examples

### Playing Music

```
User: !join
Bot: Joined voice channel ✅

User: !play https://www.youtube.com/watch?v=dQw4w9WgXcQ
Bot: 🎵 Now Playing: Rick Astley - Never Gonna Give You Up

User: !play Darude Sandstorm
Bot: ✅ Added to queue: Darude - Sandstorm (Position: 1)
```

### Managing Queue

```
User: !queue
Bot: 📃 Current Queue (2 songs):
     1. Darude - Sandstorm (4:32)
     2. The Beatles - Here Comes The Sun (3:05)

User: !skip
Bot: ⏭️ Skipped to: Darude - Sandstorm
```

### Volume Control

```
User: !volume 80
Bot: 🔊 Volume set to 80%

User: !pause
Bot: ⏸️ Playback paused

User: !resume
Bot: ▶️ Playback resumed
```

## Advanced Features

### Playlist Support

The bot supports YouTube playlists:

```
!play https://www.youtube.com/playlist?list=PLAYLIST_ID
```

### Search Functionality

Search YouTube directly:

```
!play top songs 2024
```

The bot will automatically select the first search result.

## Troubleshooting

### FFmpeg Not Found

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**Solution**:
1. Install FFmpeg (see Prerequisites)
2. Verify installation: `ffmpeg -version`
3. Ensure FFmpeg is in system PATH

### YouTube Download Fails

**Error**: `ERROR: Unable to extract video data`

**Solution**:
1. Update yt-dlp: `pip install --upgrade yt-dlp`
2. Check if the video is region-locked or age-restricted
3. Try a different video

### Bot Stuck in Voice Channel

**Error**: Bot doesn't leave after queue ends

**Solution**:
- Use `!leave` to force disconnect
- Check `auto_disconnect_timeout` in config.toml
- Restart the bot: `multicord bot restart my-music-bot`

### No Audio Playback

**Error**: Bot joins but no sound plays

**Solution**:
1. Check bot has "Speak" permission
2. Verify volume is not 0: `!volume 50`
3. Ensure FFmpeg is correctly installed
4. Check bot role isn't muted in voice channel

### Permission Errors

**Error**: `Missing Permissions` when trying to join

**Solution**:
- Verify bot has "Connect" and "Speak" permissions
- Check voice channel user limit (bot needs access)
- Ensure bot isn't banned from the channel

## Performance Notes

- **Caching**: Song metadata is cached to improve performance
- **Concurrent Bots**: When running multiple music bots, ensure each has a unique port
- **Memory Usage**: Queue size affects memory usage (configure `max_queue_size`)
- **Network**: YouTube downloads require stable internet connection

## Dependencies

This template requires:

```txt
discord.py>=2.3.0    # Discord API wrapper
yt-dlp>=2023.3.4     # YouTube downloader
PyNaCl>=1.5.0        # Voice support
toml>=0.10.2         # Config parsing
```

## Customization

### Custom Audio Sources

Add support for other platforms (Spotify, SoundCloud):

```python
# In bot.py
if 'spotify.com' in url:
    # Spotify integration code
    pass
```

### Adding Effects

Implement audio effects:

```python
from discord import FFmpegPCMAudio

# Add bass boost
ffmpeg_options = {
    'options': '-vn -af "bass=g=10"'
}
```

### Queue Limits

Modify queue behavior in config:

```toml
[music]
max_queue_size = 100
allow_duplicates = false
loop_mode = "none"  # none, single, queue
```

## Known Limitations

- Maximum song length: 10 minutes (YouTube restriction)
- YouTube rate limiting may occur with heavy usage
- Some region-locked content cannot be played
- Live streams have limited support

## License

MIT License - see root repository LICENSE file

---

**Made with [MultiCord](https://github.com/HollowTheSilver/MultiCord)** | [Report Issues](https://github.com/HollowTheSilver/MultiCord-Templates/issues)
