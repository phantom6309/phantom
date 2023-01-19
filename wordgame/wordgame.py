# -*- coding: utf-8 -*-
from redbot.core.commands import Cog
from redbot.core.data_manager import bundled_data_path
from redbot.core import Config, commands
import discord
from collections import defaultdict
from random import randint
import random

class Wordgame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.game_channel = None
        self.current_word = ""
        self.previous_user = None
        self.winning_score = "400"
        self.scores = defaultdict(int)
        self.used_words = set()
        self.word_list = self.load_word_list()

    def load_word_list(self):
        word_list_path = bundled_data_path(self) / "wordlist.txt"
        with open(word_list_path) as f:
            return [line.strip() for line in f]


    @commands.command()
    async def wordgame_start(self, ctx):
        self.current_word = random.choice(self.word_list)
        self.used_words.clear()
        await ctx.send(f"The game has started! The current word is: {self.current_word}")

    @commands.command()
    async def wordgame_channel(self, ctx, channel: discord.TextChannel):
        self.game_channel = channel
        await ctx.send(f"The game will be played in {channel.mention}")

    @commands.command()
    async def wordgame_score(self, ctx):
        scores = "\n".join(f"{self.bot.get_user(user_id)}: {score}" for user_id, score in self.scores.items())
        await ctx.send(f"Scores:\n{scores}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel != self.game_channel or message.author == self.bot.user:
            return
        if message.content.startswith(self.current_word[-1]) and message.content in self.word_list and message.content not in self.used_words:
            self.used_words.add(message.content)
            self.scores[message.author.id] += len(message.content)
            self.current_word = random.choice(self.word_list)
            await message.channel.send(f"Correct! The new word is: {self.current_word}")
        else:
            self.scores[message.author.id] -= len(message.content)
            await message.channel.send("Incorrect! Please try again.")
    @commands.command()
    async def wordgame_end(self, ctx):
        self.game_channel = None
        self.current_word = ""
        self.scores.clear()
        self.used_words.clear()
        await ctx.send("The game has ended.")

