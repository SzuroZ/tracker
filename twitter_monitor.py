import random
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from config import PROXIES, USER_AGENTS

class TwitterMonitor:
    def __init__(self, proxies=PROXIES, user_agents=USER_AGENTS, tracked_accounts=None, refresh_rate=10):
        self.proxies = proxies
        self.user_agents = user_agents
        self.tracked_accounts = tracked_accounts or []
        self.refresh_rate = refresh_rate
        self.last_seen = {}

    def get_random_proxy(self):
        """Véletlenszerű proxy kiválasztása."""
        return random.choice(self.proxies)

    def get_random_user_agent(self):
        """Véletlenszerű User-Agent kiválasztása."""
        return random.choice(self.user_agents)

    def fetch_tweet(self, username):
        """Scrape tweetek az adott felhasználó oldaláról Playwright használatával."""
        url = f"https://twitter.com/{username}"
        proxy = self.get_random_proxy()
        user_agent = self.get_random_user_agent()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Launch browser in headless mode
            context = browser.new_context(
                user_agent=user_agent,
                proxy={"server": proxy}
            )
            page = context.new_page()
            page.goto(url)
            page.wait_for_selector('article')  # Wait for tweets to load
            html_content = page.content()
            browser.close()

        return self.extract_tweets(html_content)

    def extract_tweets(self, html):
        """Kivonja a tweetek adatokat a HTML-ból."""
        soup = BeautifulSoup(html, 'html.parser')
        tweets = []

        # Mivel a tweetek dinamikusan töltődnek, azokat kereshetjük az 'article' tagekben.
        for tweet in soup.find_all('article'):
            tweet_text = tweet.find('div', {'lang': True}).get_text() if tweet.find('div', {'lang': True}) else ''
            tweet_link = tweet.find('a', {'href': True})
            tweet_image_url = tweet.find('img', {'src': True})['src'] if tweet.find('img', {'src': True}) else None
            tweet_link = f"https://twitter.com{tweet_link['href']}" if tweet_link else None
            tweets.append({
                'text': tweet_text,
                'link': tweet_link,
                'image': tweet_image_url
            })
        return tweets

    def check_new_tweets(self, username):
        """Frissíti a fiókot és visszaadja az új tweeteket."""
        new_tweets = self.fetch_tweet(username)
        return new_tweets

    def monitor_twitter(self):
        """Folyamatosan figyeli a hozzáadott fiókokat és értesíti a Discord botot."""
        while True:
            for account in self.tracked_accounts:
                new_tweets = self.check_new_tweets(account)
                if new_tweets:
                    for tweet in new_tweets:
                        print(f"New tweet from {account}: {tweet['text']} - {tweet['link']}")
                        # Itt elküldhetjük a Discord botnak a tweetet
                        # discord_bot.send_tweet_to_discord(tweet)  # Ehhez a botot implementálni kell
            time.sleep(self.refresh_rate)
