import discord
import aiohttp
import random
import os
from discord.ext import commands

STEAM_TOKEN = os.getenv('STEAM_API_TOKEN')
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

class SteamHandler:

    def __init__(self, token: str):
        self.token = token

    async def get_games_by_id(self, id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={self.token}&steamid={id}&format=json&include_appinfo=true') as response:
                resp = await response.json()
        if "games" not in resp["response"]:
            raise Exception("No games found")
        return list(map(lambda x: x["name"], resp["response"]["games"]))

inten = discord.Intents.default()
inten.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=inten)
steam = SteamHandler(STEAM_TOKEN)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)

@bot.command()
async def roulette(ctx: commands.Context, steam_ids: commands.Greedy[int]):
    if len(steam_ids) < 2: # We need at least 2 id's to Compare
        await ctx.send("Please provide at least 2 steam ids")
        return
    filtered_games = []

    someone_messed_up_the_fun = None

    for id in steam_ids:
        try:
            games = await steam.get_games_by_id(id)
        except Exception as e:
            someone_messed_up_the_fun = id
            continue
        if not games:
            someone_messed_up_the_fun = id
            continue
        if len(filtered_games) == 0 and not someone_messed_up_the_fun:
            filtered_games = games
            continue
        filtered_games = list(set(filtered_games) & set(games))
    
    if someone_messed_up_the_fun:
        await ctx.send(f"Couldn't find games for {someone_messed_up_the_fun}")

    selected_game = random.choice(filtered_games)
    await ctx.reply(f'Play {selected_game}!')

bot.run(BOT_TOKEN)