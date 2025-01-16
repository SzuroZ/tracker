import discord
from discord.ext import commands
from config import DISCORD_TOKEN, TRACKED_ACCOUNTS

class DiscordBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_account(self, ctx, account_name):
        """Hozzáad egy új Twitter fiókot a figyeléshez."""
        if account_name not in TRACKED_ACCOUNTS:
            TRACKED_ACCOUNTS.append(account_name)
            await ctx.send(f"Fiók hozzáadva: {account_name}")
        else:
            await ctx.send(f"Ez a fiók már figyelve van: {account_name}")

    @commands.command()
    async def remove_account(self, ctx, account_name):
        """Eltávolít egy figyelt Twitter fiókot."""
        if account_name in TRACKED_ACCOUNTS:
            TRACKED_ACCOUNTS.remove(account_name)
            await ctx.send(f"Fiók eltávolítva: {account_name}")
        else:
            await ctx.send(f"Ez a fiók nem található: {account_name}")

    @commands.command()
    async def list_accounts(self, ctx):
        """Listázza az összes figyelt fiókot."""
        await ctx.send(f"Jelenleg figyelt fiókok: {', '.join(TRACKED_ACCOUNTS)}")

    async def send_tweet_to_discord(self, tweet):
        """Küld egy tweetet Discordra."""
        channel = self.bot.get_channel(123456789012345678)  # Cseréld le a csatorna ID-jára
        embed = discord.Embed(title="New Tweet!", description=tweet['text'], url=tweet['link'])
        if tweet['image']:
            embed.set_image(url=tweet['image'])
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(DiscordBot(bot))
