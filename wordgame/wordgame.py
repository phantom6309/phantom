# -*- coding: utf-8 -*-
from redbot.core.commands import Cog
from redbot.core.data_manager import bundled_data_path
from redbot.core import Config, commands
import discord
import sqlite3
from collections import defaultdict
from random import randint
import random

class Kelime(commands.Cog):
    """Son kelimenin son harfi ile kelime uydurma oyunu."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(self, identifier=545846965)
        default_global = {"scores": {}}
        self.config.register_global(**default_global)
        self.game_channel = None
        self.current_word = ""
        self.previous_user = None
        self.winning_score = None
        self.word_list = self.load_word_list()
        self.conn = sqlite3.connect("scores.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS scores (user_id INTEGER PRIMARY KEY, score INTEGER)"
        )
        self.conn.commit()
        self.scores = defaultdict(int)
    def load_word_list(self):
        word_list_path = bundled_data_path(self) / "wordlist.txt"
        with open(word_list_path) as f:
            return [line.strip() for line in f]

    async def give_points(self, user: discord.User, word: str, message):
    # Compare the user who played the previous word to the current user
     if self.previous_user == user:
        await self.game_channel.send(f"Lütfen bekleyin, sıradaki oyuncu oynasın.")
        await self.game_channel.send(f"Son kelime: {self.current_word}")
        return

    # Update the previous_user variable
     self.previous_user = user

     if word in self.used_words:
        self.scores[user.id] -= len(word)
        await self.game_channel.send(f"{word} kelimesi zaten kullanılmış.Yedin eksiyi.")
        emoji2 = '\N{THUMBS DOWN SIGN}'
        await message.add_reaction(emoji2)
        await self.game_channel.send(f"Son kelime: {self.current_word}")
     if word[-1] == "ğ":
        # Select a random word from the continue_words list
        new_word = self.word_list[randint(
                0, len(self.word_list) - 1)]
        # Add the new word to the used words list
        self.used_words.append(new_word)
        # Set the current word to the new word
        self.current_word = new_word
        await self.game_channel.send(f"{word} kelimesiyle biten kelime oynayamazsınız. Sıradaki kelime: {self.current_word}")
     if word in self.word_list and word not in self.used_words:
        self.used_words.append(word)
        self.current_word = word
        self.scores[user.id] += len(word)
        emoji = '\N{THUMBS UP SIGN}'
        await message.add_reaction(emoji)



    async def remove_points(self, user: discord.User, word: str, message):
        self.scores[user.id] -= len(word)
        emoji2 = '\N{THUMBS DOWN SIGN}'
        await message.add_reaction(emoji2)
        await self.game_channel.send(f"Son kelime: {self.current_word}")
        if word not in self.word_list:
            await self.game_channel.send(f"geçersiz")

    @commands.command()
    async def kelimekanal(self, ctx, channel: discord.TextChannel):
        """Kelime Oyunu için kanal seçimi"""
        self.game_channel = channel
        await ctx.send(f"Seçilen oyun kanalı {channel.mention}.")

    @commands.command()
    async def kelimehedef(self, ctx, score: int):
        """Oyun bitim skoru seçimi"""
        self.winning_score = score
        await ctx.send(f"Seçilen kazanma skoru {score}.")

    @commands.command()
    async def kelimeekle(self, ctx, *, word: str):
        """Listeye kelime ekleyin"""
        self.word_list.append(word.lower())
        await ctx.send(f"{word} listeye eklendi.")

    async def update_scores(self):
        self.cursor.execute("DELETE FROM scores")
        for user_id, score in self.scores.items():
            self.cursor.execute(
                "INSERT INTO scores VALUES (?, ?)", (user_id, score))
        self.conn.commit()

    @commands.command()
    async def liderlik(self, ctx):
        """Liderlik durumunu görün"""
        self.cursor.execute("SELECT * FROM scores ORDER BY score DESC")
        scores = self.cursor.fetchall()
        message = "Top scores:\n"
        for i, (player_id, score) in enumerate(scores):
            player = self.bot.get_user(player_id)
            if player is not None:
                message += f"{i + 1}. {player} - {score}\n"
            else:
                message += f"{i + 1}. Unknown player ({player_id}) - {score}\n"
        await ctx.send(message)

    def last_author(self):
        word_list_path = bundled_data_path(self) / "wordlist.txt"
        with open(word_list_path) as f:
            return [line.strip() for line in f]
    @commands.command()
    async def kelimebaşla(self, ctx):
        """Oyunu başlatın"""
        self.used_words = []
        if self.game_channel is None:
            self.game_channel = ctx.channel
            self.current_word = self.word_list[randint(
                0, len(self.word_list) - 1)]
            self.winning_score = None
            self.scores = defaultdict(int)
            await ctx.send(f"Yeni oyun {ctx.channel.mention} kanalında başladı!")
            await ctx.send(f"Başlangıç kelimesi: {self.current_word}")
        else:
            self.current_word = self.word_list[randint(
                0, len(self.word_list) - 1)]
            self.winning_score = None
            self.scores = defaultdict(int)
            channel2 = self.game_channel
            await ctx.send(f"Yeni oyun {channel2} kanalında başladı!")
            await channel2.send(f"Başlangıç kelimesi: {self.current_word}")


    @Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.channel == self.game_channel and not message.content.startswith("."):
            kek = message.content.strip()
            lower_map = {
                ord(u'I'): u'ı',
                ord(u'İ'): u'i',
            }
            test = kek.translate(lower_map)
            word = test.lower()
            if self.current_word and word[0].startswith(self.current_word[-1]) and word in self.word_list:
                
                await self.give_points(message.author, word, message)
                if self.winning_score is not None:
                    user_score = self.scores[message.author.id]
                    if user_score >= self.winning_score:
                        await message.channel.send(
                            f"{message.author} kazandı.Skoru {user_score}!"
                        )
                        await self.update_scores()
                        self.game_channel = None
                        self.current_word = ""
                        self.winning_score = None
                        self.scores = defaultdict(int)
            else:
                await self.remove_points(message.author, word, message)

    @commands.command()
    async def kelimedurdur(self, ctx):
        """Oyunu durdurun"""
        if self.game_channel is not None:
            self.game_channel = None
            self.current_word = ""
            self.winning_score = None
            self.scores = defaultdict(int)
            await ctx.send("Oyun durduruldu.")
        else:
            await ctx.send("Açık oyun yok.")

    @commands.command()
    async def kelimeson(self, ctx):
        """Son yazılan kelimeyi görün"""
        if self.current_word:
            await ctx.send(f"Son kelime: {self.current_word}")
        else:
            await ctx.send("Açık oyun yok.")

    @commands.command()
    async def skor(self, ctx, user: discord.User = None):
        """Mevcut oyunun puan durumu"""
        if self.current_word:
            if user is not None:
                score = self.scores[user.id]
                await ctx.send(f"{user}'nin puanı {score}.")
            else:
                await ctx.send(f"Puanınız {self.scores[ctx.author.id]}.")
        else:
            await ctx.send("Açık oyun yok.")

    @commands.command()
    async def kelimesayısı(self, ctx):
        """Toplam kelime sayısını görüntüeyin"""
        word_count = len(self.word_list)
        await ctx.send(f"Listede şuanda {word_count} kelime bulunuyor.")
