# Discord Verification Bot

This Python bot verifies users on Discord using student IDs and verification codes.

## Prerequisites

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

## Cloning the Repository & cd the directory & creating `.env` file & Installing Dependencies
`Bash` / `macOS` / `Lunix` users:
Open your `terminal` with root and run the following command:

```bash
git clone https://github.com/ambish-creature/a_test-discord-bot.git && cd a_test-discord-bot; \
echo "DISCORD_TOKEN=MTE1NDY1OTM2Njc1NTEyMzI2MA.GH_ftP.KNasarORC-iMpq9GbwtdQgaI_HzbXRP8Adjb9k" > .env; \
echo "CHATGPT_API_KEY=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" >> .env; \
pip install -r requirements.txt
```

### Run the bot:

```bash
python main.py
```

The Discord bot should now be up and running.
