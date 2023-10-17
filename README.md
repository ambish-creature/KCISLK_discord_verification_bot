# Discord Verification Bot

This Python bot verifies users on Discord using student IDs and verification codes.

## Requirements

Before running this bot, ensure you have the following installed on your system:

- [Homebrew](https://brew.sh/) for `bash` users:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- [Python 3](https://www.python.org/downloads/) for `bash` users:

```bash
curl -LO https://www.python.org/ftp/python/3.12.0/python-3.12.0-macos11.pkg && \
sudo installer -pkg python-3.12.0-macos11.pkg -target /
```
Or install through homebrew:

```bash
brew install python
```

- [Git](https://git-scm.com/) for `bash` users:

```bash
brew install git
```

## Getting Started

## Cloning the Repository & cd the directory & Installing Dependencies
`Bash` / `macOS` / `Lunix` users:
Open your `terminal` with root / administrator and run the following command:

```bash
git clone https://github.com/ambish-creature/KCISLK_discord_verification_bot.git && cd KCISLK_discord_verification_bot; \
pip install discord discord.py discord-py-slash-command
```
### Change the bot code:
open `bot0.py`, find the line "TOKEN", and replece the token with the one I've sent on the discord group.

### Run the bot:

```bash
cd KCISLK_discord_verification_bot && python bot0.py
```

The Discord bot should now be up and running.

`Windows` users:

For Windows users, follow these steps to set up the bot:

1. **Install Python 3:**
   - Download the installer from [Python's official website](https://www.python.org/downloads/).
   - During installation, make sure to check the box that says "Add Python 3.x to PATH".

2. **Install Git:**
   - Download the installer from [Git's official website](https://git-scm.com/).
   - Follow the installation instructions provided by the installer.

3. **Clone the Repository & Install Dependencies:**
   - Open the command prompt or PowerShell with administrator privileges.
   - Run the following commands:

   ```bash
   git clone https://github.com/ambish-creature/KCISLK_discord_verification_bot.git
   cd KCISLK_discord_verification_bot
   pip install discord discord.py discord-py-slash-command
   ```
### Change the bot code:
open `bot0.py`, find the line "TOKEN", and replece the token with the one I've sent on the discord group.

### Run the bot:

```bash
cd KCISLK_discord_verification_bot
python bot0.py
```

The Discord bot should now be up and running.
