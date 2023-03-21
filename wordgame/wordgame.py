# -*- coding: utf-8 -*-
import discord
from datetime import datetime
from redbot.core import commands, Config
from typing import Optional

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)

    @commands.command()
    async def profil(self, ctx, member: Optional[discord.Member] = None):
        """Creates or shows user profile."""
        if member is None:
            member = ctx.author

        user_data = await self.config.user(member).all()
        if not user_data:
            await self.create_profile(member)
            user_data = await self.config.user(member).all()

        embed = discord.Embed(title=f"{member.name}'s profile", color=member.color)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"ID: {member.id}")
        fields = [("Age", user_data.get("age", "N/A")),
                  ("School", user_data.get("school", "N/A")),
                  ("Hobbies", user_data.get("hobbies", "N/A")),
                  ("Favorite TV show", user_data.get("favorite_tv_show", "N/A")),
                  ("Favorite movie", user_data.get("favorite_movie", "N/A")),
                  ("Role", user_data.get("role", "N/A")),
                  ("Time in server", self.time_in_server(member))]

        for name, value in fields:
            if value != "pas":
                embed.add_field(name=name, value=value, inline=False)

        await ctx.send(embed=embed)

    async def create_profile(self, member):
        """Asks the user questions to create a profile."""
        questions = {"age": "What's your age?",
                     "school": "What school do you go to?",
                     "hobbies": "What are your hobbies?",
                     "favorite_tv_show": "What's your favorite TV show?",
                     "favorite_movie": "What's your favorite movie?",
                     "role": "What's your role in the server? (ex: Moderator, Admin, etc.)",
                     "time_in_server": self.time_in_server(member)}
        data = {}
        for key, question in questions.items():
            if key == "time_in_server":
                data[key] = question
            else:
                await member.send(question)
                response = await self.bot.wait_for("message", check=lambda m: m.author == member)
                if response.content.lower() != "pas":
                    data[key] = response.content
        await self.config.user(member).set(data)

    def time_in_server(self, member):
        time_in_server = datetime.now() - member.joined_at
        return str(time_in_server).split('.')[0]

