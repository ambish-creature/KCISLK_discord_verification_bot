# main.py
import bot
import asyncio

if __name__ == '__main__':
    asyncio.run(bot.client.run(bot.TOKEN))