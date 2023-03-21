# -*- coding: utf-8 -*-
import discord
from redbot.core import commands
from redbot.core import Config

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=7895645342)
        self.config.register_member(age=None, school=None, hobbies=None, favorite_tv_show=None, favorite_movie=None)

    @commands.group()
    async def profil(self, ctx: commands.Context) -> None:
        """Profilinizi oluşturun veya başka birinin profilini görüntüleyin """
        pass

    @profil.command(name="oluştur")
    async def _oluştur(self, ctx):
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

    
    @profil.command(name="soru-ekle")
    async def _soru_ekle(self, ctx):
     await ctx.author.send("Lütfen eklemek istediğiniz soruyu yazın.")
     question = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
     await self.config.set_raw("questions", str(len(await self.config.questions())), value=question.content)
     await ctx.send("Soru başarıyla eklendi!")

    @profil.command(name="değiştir")
    async def _değiştir(self, ctx, field: str):
     fields = {
        "yaş": "age",
        "okul": "school",
        "hobiler": "hobbies",
        "en sevdiğiniz tv programı": "favorite_tv_show",
        "en sevdiğiniz film": "favorite_movie"
     }
     field = fields.get(field.lower())
     if not field:
        return await ctx.send("Geçersiz alan adı!")
     await ctx.author.send(f"Lütfen yeni {field} değerini girin.")
     value = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
     await self.config.member(ctx.author).set_raw(field, value=value.content)
     await ctx.send(f"{field} değeri başarıyla güncellendi!")

    @profil.command(name="göster")
    async def _göster(self, ctx, member: discord.Member):
        if member is None:
        # If no member is specified, use the author of the message as the member
           member = ctx.author
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
         embed.set_image(url=member.avatar_url_as(size=1024))
         await ctx.send(embed=embed)
