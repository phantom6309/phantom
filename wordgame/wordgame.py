# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
from redbot.core import Config

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7895645342)
        self.config.register_member(age=None, school=None, hobbies=None, favorite_tv_show=None, favorite_movie=None)
    
    @commands.command()
    async def profil_oluştur(self, ctx):
        await ctx.author.send("Merhaba, profilinizi oluşturmak için birkaç soru sormak istiyoruz. Lütfen yaşınızı söyler misiniz?")
        age = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("Hangi okulda okuyorsunuz?")
        school = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("Hangi hobileriniz var?")
        hobbies = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("En sevdiğiniz TV programı nedir?")
        favorite_tv_show = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await ctx.author.send("En sevdiğiniz film nedir?")
        favorite_movie = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        
        await self.config.member(ctx.author).age.set(age.content)
        await self.config.member(ctx.author).school.set(school.content)
        await self.config.member(ctx.author).hobbies.set(hobbies.content)
        await self.config.member(ctx.author).favorite_tv_show.set(favorite_tv_show.content)
        await self.config.member(ctx.author).favorite_movie.set(favorite_movie.content)
        
        await ctx.send("Profiliniz başarıyla oluşturuldu!")
    
    @commands.command()
    async def profil_göster(self, ctx, member: discord.Member):
        age = await self.config.member(member).age()
        school = await self.config.member(member).school()
        hobbies = await self.config.member(member).hobbies()
        favorite_tv_show = await self.config.member(member).favorite_tv_show()
        favorite_movie = await self.config.member(member).favorite_movie()
        
        embed = discord.Embed(title=f"{member.display_name}'s Profile", color=0x00ff00)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Yaş", value=age or "Bilinmiyor")
        embed.add_field(name="Okul", value=school or "Bilinmiyor")
        embed.add_field(name="Hobiler", value=hobbies or "Bilinmiyor")
        embed.add_field(name="En Sevdiğiniz TV Programı", value=favorite_tv_show or "Bilinmiyor")
        embed.add_field(name="En Sevdiğiniz Film", value=favorite_movie or "Bilinmiyor")
        
        await ctx.send(embed=embed)
