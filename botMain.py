import discord
import os
import PIL
from os.path import exists
from discord.ext import commands
from bimsolutions import bimsolutions

# Variables
bot = commands.Bot(command_prefix='bim.')
filename = "answer.png" # Has to end in .png
# Colors
bot.colorError = discord.Color.red()
bot.colorSuccess = discord.Color.green()
bot.colorWarning = discord.Color.yellow()
bot.colorInfo = discord.Color.blue()

# Make sure the bot is in the same directory as this script
if os.path.dirname(os.path.abspath(__file__)) != os.path.abspath(os.getcwd()):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Make sure token works properly
if not exists("token.txt"):
    with open("token.txt", "w") as f:
        while True:
            token = input("Enter your bot token: ")
            if len(token) == 59:
                f.write(token)
                break
            else:
                print("Invalid token length. Please try again.")
else:
    with open("token.txt", "r") as f:
        token = f.read()
        if len(token) != 59:
            while True:
                token = input("Invalid token length. Please try again: ")
                if len(token) == 59:
                    with open("token.txt", "w") as f:
                        f.write(token)
                    break
                else:
                    print("Invalid token length. Please try again.")


def embedMaker(title, description, color, image = None):
    embed = discord.Embed(title=title, description=description, color=color)
    if image != None:
        embed.set_image(url=image)
    return embed
    
# Show message on bot login
@bot.event
async def on_ready():
    print(f"Bot started as {bot.user}")

@bot.command(alias=['answer'])
async def answer(ctx, book = None, chapter = None, lesson = None, question = None):
    if any(x is None for x in [book, chapter, lesson, question]):
        await ctx.send("Error: Please enter all arguments.")
        return
    else:
        answer = str(bimsolutions(book, chapter, lesson, question, filename))
        if answer.startswith("Error"):
            await ctx.send(embed=embedMaker(title="Error!", description=answer, color=bot.colorError))
        else:
            print(answer)
            file = discord.File(os.path.abspath(filename), filename=filename)
            await ctx.send(file=file, embed=embedMaker(title="Answer Found!", description=None, color=bot.colorSuccess, image="attachment://" + filename))
bot.run(token)
