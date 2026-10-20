import discord
from discord.ext import commands
import random
import os
from threading import Thread
from flask import Flask

# -------------------- 🌐 إعداد موقع ولوحة التحكم المدمجة لضمان 24/7 --------------------
app = Flask('')

@app.route('/')
def home():
    return "<h1>🏴‍☠️ 𝐑𝐄𝐐𝐔𝐈𝐄𝐌 BOT IS ONLINE & RUNNING 24/7 ❄️</h1>"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# -------------------- ⚙️ إعدادات الصلاحيات والبوت --------------------
intents = discord.Intents.default()
intents.members = True          # رصد دخول وخروج الأعضاء
intents.message_content = True  # قراءة الأوامر

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# الآيديات المعتمدة لسيرفرك:
WELCOME_CHANNEL_ID = 1229330192087121953
GOODBYE_CHANNEL_ID = 1229334036737167412
AUTO_ROLE_ID = 1506672295970865263
BANNER_URL = "https://i.ibb.co/3s68R3N/watermarked-img-6138380908856298660.jpg"

@bot.event
async def on_ready():
    print(f"✅ تم تشغيل البوت بنجاح! الاسم: {bot.user.name}")
    await bot.change_presence(
        activity=discord.Game(name="🏴‍☠️ 𝐑𝐄𝐐𝐔𝐈𝐄𝐌 CREW | !help")
    )

# -------------------- ❄️ نظام الترحيب والخروج --------------------
@bot.event
async def on_member_join(member: discord.Member):
    # إعطاء الرتبة التلقائية
    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
        except Exception as e:
            print(f"خطأ في إعطاء الرتبة: {e}")

    # إرسال كارت الترحيب
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="❄️ WELCOME TO THE REQUIEM CREW 🏴‍☠️",
            description=f"أهلاً بك يا قرصان {member.mention} في **{member.guild.name}**!\n\n"
                        f"⚓ أنت العضو رقم **#{member.guild.member_count}** في الطاقم.\n"
                        f"جهّز تشكيلاتك في **One Piece Bounty Rush** واستعد للمعارك! 🔥",
            color=discord.Color.from_rgb(0, 162, 255)
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        if BANNER_URL:
            embed.set_image(url=BANNER_URL)
        embed.set_footer(text="OUR ETERNAL KINGDOM AWAITS ❄️")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member: discord.Member):
    channel = member.guild.get_channel(GOODBYE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🏴‍☠️ غادر أحد القراصنة",
            description=f"العضو **{member.name}** غادر الطاقم وسيرفر **{member.guild.name}**...\n"
                        f"نتمنى لك التوفيق في رحلتك القادمة! 🌊",
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="REQUIEM CREW ❄️")
        await channel.send(embed=embed)

# -------------------- 📜 قائمة المساعدة والمساعدة الأنيقة --------------------
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="🏴‍☠️ قائمة أوامر 𝐑𝐄𝐐𝐔𝐈𝐄𝐌 𝐁𝐎𝐓",
        description="إليك جميع الأوامر المتاحة للاستخدام في السيرفر:",
        color=discord.Color.gold()
    )
    embed.add_field(name="🛡️ أوامر الإدارة", value="`!clear [عدد]` - مسح الرسائل\n`!kick [عضو]` - طرد عضو\n`!ban [عضو]` - حظر عضو", inline=False)
    embed.add_field(name="🎮 أوامر التفاعل وبونتي", value="`!profile` - عرض بطاقتك\n`!character` - سحب شخصية ون بيس عشوائية\n`!serverinfo` - معلومات السيرفر\n`!ping` - فحص سرعة البوت", inline=False)
    embed.set_footer(text="REQUIEM CREW | Bounty Rush System")
    await ctx.send(embed=embed)

# -------------------- 🛡️ أوامر الإدارة والتحكم --------------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """مسح عدد محدد من الرسائل"""
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 تم مسح **{amount}** رسالة بنجاح!", delete_after=3)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="بدون سبب"):
    """طرد عضو من السيرفر"""
    await member.kick(reason=reason)
    await ctx.send(f"👞 تم طرد העضو **{member.name}** من السيرفر! السبب: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="بدون سبب"):
    """حظر عضو من السيرفر"""
    await member.ban(reason=reason)
    await ctx.send(f"🔨 تم حظر العضو **{member.name}** بنجاح! السبب: {reason}")

# -------------------- 🎮 أوامر عامة وتفاعلية --------------------
@bot.command()
async def profile(ctx, member: discord.Member = None):
    """عرض ملف العضو في السيرفر"""
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 بطاقة القرصان: {member.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="🆔 آيدي العضو:", value=f"`{member.id}`", inline=True)
    embed.add_field(name="📅 تاريخ الانضمام:", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="🎖️ أعلى رتبة:", value=member.top_role.mention, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def character(ctx):
    """سحب شخصية عشوائية من ون بيس"""
    characters = [
        "🔥 EX Roger (Extreme Gol D. Roger)",
        "⚡ EX Shanks (FR Shanks / Film Red)",
        "🐉 EX Kaido (Hybrid Kaido)",
        "🍖 EX Gear 5 Luffy (Nika)",
        "⚔️ EX Zoro (Onigashima Zoro)",
        "❄️ EX Yamato",
        "🖤 EX Whitebeard (Light Edward Newgate)",
        "☄️ EX Akainu (Fleet Admiral)"
    ]
    chosen = random.choice(characters)
    await ctx.send(f"🎰 **{ctx.author.mention}** حظك اليوم في السحب هو:\n✨ **{chosen}** ✨")

@bot.command()
async def serverinfo(ctx):
    """معلومات سيرفر ريكويم"""
    guild = ctx.guild
    embed = discord.Embed(title=f"🏴‍☠️ معلومات طاقم {guild.name}", color=discord.Color.purple())
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="👑 صاحب السيرفر:", value=guild.owner.mention, inline=True)
    embed.add_field(name="👥 عدد الأعضاء:", value=f"**{guild.member_count}** عضو", inline=True)
    embed.add_field(name="💬 عدد الرومات:", value=f"**{len(guild.channels)}** روم", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 **السرعة:** {round(bot.latency * 1000)}ms | البوت شغال بأعلى كفاءة!")

# -------------------- 🚀 تشغيل البوت واللوحة --------------------
keep_alive() # تشغيل خادم الويب المدمج لـ 24/7
bot.run("MTU2MjA5NDg2Nzg2MDE2MDUyNA.GMMhRB.eF629tXn1Tskb1Q8aXUyiBUlAwF4oM0qsQ1p80")
