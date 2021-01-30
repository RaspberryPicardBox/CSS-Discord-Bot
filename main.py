import discord
from discord.ext import commands
import random
import urllib.request
import json

if __name__ == '__main__':
    description = "The Computer Science Society Discord bot!"

    intents = discord.Intents.default()
    intents.members = True

    bot = commands.Bot(command_prefix='!', description=description, intents=intents)


    @bot.event
    async def on_ready():
        print("Logged in as: " + bot.user.name + " " + str(bot.user.id))
        print("----\n")


    @bot.command()
    async def studentfinance(ctx):
        """Get the date of the next Student Finance payment."""
        with urllib.request.urlopen('https://studentfinancecountdown.com/json/left/') as url:
            data = json.loads(url.read().decode())

            embed = discord.Embed(title="Next payment is in {0} days!".format(data["payload"]["days"]),
                                  url="https://studentfinancecountdown.com/")

            if data["payload"]["after"] == 'This is the last payment of the year':
                embed.add_field(name="Which will be {0}".format(data["payload"]["next"]), value="{0}.".format(data["payload"]["after"]))
            else:
                embed.add_field(name="Which will be {0}".format(data["payload"]["next"]), value="Payment after is {0}.".format(data["payload"]["after"]))

            await ctx.send(embed=embed)


    @bot.command()
    async def ping(ctx):
        """Returns the latency of this bot!"""
        await ctx.send("My current response time is: {0}ms".format(round(bot.latency, 1)))


    @bot.command()
    async def changerole(ctx, newrole):
        """Changes your role to either First-Year, Second-Year, Third-Year, Postgraduate or Alumni."""
        role = discord.utils.get(ctx.guild.roles, name=newrole)
        firstRole = discord.utils.get(ctx.guild.roles, name="First-Year")
        secondRole = discord.utils.get(ctx.guild.roles, name="Second-Year")
        thirdRole = discord.utils.get(ctx.guild.roles, name="Third-Year")
        postRole = discord.utils.get(ctx.guild.roles, name="Postgraduate")
        alumRole = discord.utils.get(ctx.guild.roles, name="Alumni")
        roles = [firstRole, secondRole, thirdRole, postRole, alumRole]

        if role in ctx.author.roles:
            await ctx.send("You already have that role!")
        else:
            if role in roles:
                for currentRole in ctx.author.roles:
                    if currentRole in roles:
                        await ctx.author.remove_roles(currentRole)
                await ctx.author.add_roles(role)
                await ctx.send("{0} now has role {1}".format(ctx.author, role))
            else:
                await ctx.send(
                    "Sorry, I can't find that role. The valid roles are: First-Year, Second-Year, Third-Year, Postgraduate, and Alumni.")


    @bot.command()
    async def rollDie(ctx, numberofdice, numberofsides, modifier=None):
        """Roll a die, or dice, with any number of sides. Add a modifier, if liked."""
        if modifier is None:
            modifier = 0
        else:
            modifier = int(modifier)

        try:
            numberofdice = int(numberofdice)
            numberofsides = int(numberofsides)
            rolls = ""
            total = 0

            if numberofdice > 0:
                for i in range(numberofdice):
                    roll = round(random.randint(0, numberofsides), 1) + modifier
                    total += roll
                    rolls += "[" + str(roll) + "]" + " "
                await ctx.send(rolls)
                await ctx.send("Total: {0}".format(total))
            else:
                await ctx.send("I can't roll 0 dice. The answer is clearly 0...")
        except:
            await ctx.send("Whoopsie, something went wrong! `!help rollDie` for more info!")


    @bot.command()
    async def stop(ctx):
        """Stops the bot, if you have the right."""
        if ctx.author.id == 344911466195058699 or discord.utils.get(ctx.guild.roles, name="CSS-Committee") in ctx.author.roles:
            await ctx.send("Shutting down...")
            await bot.close()
        else:
            await ctx.send("Sorry, but you don't have the privileges to do that!")


    bot.run('token')
