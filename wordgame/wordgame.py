# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
from redbot.core import Config

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=123456789)

        # Set up default values for the config
        default_global = {
            "profiles": {}
        }
        self.config.register_global(**default_global)

    @commands.command(name="profil oluştur")
    async def create(self, ctx):
        """Creates a profile for the user"""
        author_id = str(ctx.author.id)

        # Check if the user already has a profile
        if author_id in self.config.profiles:
            await ctx.send("You already have a profile!")
            return

        # Ask the user questions
        questions = [
            "What is your age?",
            "What school do you attend?",
            "What are your hobbies?",
            "What is your favorite TV show?",
            "What is your favorite movie?"
        ]

        answers = []
        for question in questions:
            await ctx.send(question)
            response = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
            answers.append(response.content)

        # Save the profile to the config
        profile_data = {
            "age": answers[0],
            "school": answers[1],
            "hobbies": answers[2],
            "favorite_tv_show": answers[3],
            "favorite_movie": answers[4]
        }
        await self.config.profiles.set_raw(author_id, value=profile_data)
        await ctx.send("Profile created!")

    @commands.command(name="profil göster")
    async def showprofile(self, ctx, member: discord.Member = None):
        """Displays the specified user's profile"""
        if not member:
            member = ctx.author

        profile_data = await self.config.profiles.get_raw(str(member.id))

        if not profile_data:
            await ctx.send(f"{member.display_name} does not have a profile.")
            return

        # Create the embed
        embed = discord.Embed(title=f"{member.display_name}'s Profile")
        embed.add_field(name="Age", value=profile_data["age"], inline=False)
        embed.add_field(name="School", value=profile_data["school"], inline=False)
        embed.add_field(name="Hobbies", value=profile_data["hobbies"], inline=False)
        embed.add_field(name="Favorite TV Show", value=profile_data["favorite_tv_show"], inline=False)
        embed.add_field(name="Favorite Movie", value=profile_data["favorite_movie"], inline=False)

        await ctx.send(embed=embed)
