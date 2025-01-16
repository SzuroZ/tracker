from twitter_monitor import TwitterMonitor
from discord_bot import DiscordBot
from config import PROXIES, USER_AGENTS, TRACKED_ACCOUNTS, DISCORD_TOKEN
import threading

def start_twitter_monitor():
    twitter_monitor = TwitterMonitor(PROXIES, USER_AGENTS, TRACKED_ACCOUNTS)
    twitter_monitor.monitor_twitter()

def start_discord_bot():
    discord_bot = DiscordBot(DISCORD_TOKEN, TRACKED_ACCOUNTS)
    discord_bot.run()

if __name__ == "__main__":
    twitter_thread = threading.Thread(target=start_twitter_monitor)
    twitter_thread.daemon = True
    twitter_thread.start()

    start_discord_bot()
