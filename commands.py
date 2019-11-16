from discord.ext import commands
from config import bot as config_bot
from db import open_db, update_db
import json

bot = commands.Bot(command_prefix=config_bot['prefix'])


@bot.command(name='паспорт')
async def passport(ctx):
    data = open_db("database/passports.json")
    user = str(ctx.author)
    if user in data:
        money = data[user]["coin"]
        await ctx.send('Деньги: ' + str(money))
    else:
        data[user] = {
            'coin': 0
        }
        update_db("database/passports.json", data)
        await ctx.send(ctx.author.name + ' Получил паспорт')


@bot.command(name='заказ')
async def drink_order(ctx, drink):
    data = open_db("database/passports.json")
    data_bar = open_db("database/bar.json")
    items = open_db("database/items.json")
    drinks = items["drinks"]
    user_name = str(ctx.author)
    user = data[user_name]
    if drink in drinks:
        if user["coin"] >= drinks[drink]["cost"]:
            order = data_bar["order"]
            if user_name not in data_bar["order"]:
                order[user_name] = []
            order[user_name].append(drink)
            update_db("bar.json", data_bar)
            await ctx.send(ctx.author.name + ' заказал ' + drink)
            return
    menu = ''
    for drink_menu in drinks:
        drink_menu_str = str(drink_menu)
        menu = menu + drink_menu_str + ': ' + str(drinks[drink_menu_str]["cost"]) + '\n'
    await ctx.send(ctx.author.name + ': \n' + menu)


bot.run(config_bot['token'])
