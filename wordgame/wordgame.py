# -*- coding: utf-8 -*-
import discord
from redbot.core import Config, commands

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=6743567823)

    @commands.command()
    async def profil_oluştur(self, ctx):
        """Asks user for profile information and saves it to config"""
        questions = ["What is your age?", "What school do you attend?", "What are your hobbies?", "What is your favorite TV show?", "What is your favorite movie?"]
        answers = []
        for question in questions:
            await ctx.send(question)
            try:
                message = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout=30.0)
                answers.append(message.content)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to answer, please try again later.")
                return
        user_id = str(ctx.author.id)
        await self.config.user_from_id(user_id).age.set(answers[0])
        await self.config.user_from_id(user_id).school.set(answers[1])
        await self.config.user_from_id(user_id).hobbies.set(answers[2])
        await self.config.user_from_id(user_id).favorite_tv_show.set(answers[3])
        await self.config.user_from_id(user_id).favorite_movie.set(answers[4])
        await ctx.send("Your profile has been created!")

    @commands.command()
    async def profil_göster(self, ctx, member: discord.Member = None):
        """Shows the profile information for a given user"""
        if not member:
            member = ctx.author
        user_id = str(member.id)
        age = await self.config.user_from_id(user_id).age()
        school = await self.config.user_from_id(user_id).school()
        hobbies = await self.config.user_from_id(user_id).hobbies()
        favorite_tv_show = await self.config.user_from_id(user_id).favorite_tv_show()
        favorite_movie = await self.config.user_from_id(user_id).favorite_movie()

        embed = discord.Embed(title=f"{member.name}'s profile")
        embed.add_field(name="Age", value=age, inline=False)
        embed.add_field(name="School", value=school, inline=False)
        embed.add_field(name="Hobbies", value=hobbies, inline=False)
        embed.add_field(name="Favorite TV Show", value=favorite_tv_show, inline=False)
        embed.add_field(name="Favorite Movie", value=favorite_movie, inline=False)

        await ctx.send(embed=embed)
