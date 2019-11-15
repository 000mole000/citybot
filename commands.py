from discord.ext import commands
from config import bot as config_bot
import json

bot = commands.Bot(command_prefix=config_bot['prefix'])


@bot.command(name='паспорт')
async def passport(ctx):
    passports = open("passports.json", "r")
    passports_str = passports.read()
    data = json.loads(passports_str)
    user = str(ctx.author)
    passports.close()
    if user in data:
        money = data[user]["coin"]
        await ctx.send('Деньги: '+str(money))
    else:
        add_user = open("passports.json", "w")
        data[user] = {
            'coin': 0
        }
        data = json.dumps(data)
        add_user.write(data)
        add_user.close()
        await ctx.send(ctx.author.name + ' Получил паспорт')


bot.run(config_bot['token'])
