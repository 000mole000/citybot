import asyncio

import discord
from discord.ext import commands
from config import bot as config_bot
from db import open_db, update_db
import json

bot = commands.Bot(command_prefix=config_bot['prefix'])


@bot.command(name='помощь')
async def help_commands(ctx):
    await ctx.send(
        '**Команды**```py\n@ Oбщие:\n\'!паспорт\' - создает паспорт ,если он уже есть выводит данные пользователя\n\''
        '!заказ <название>\' - заказ в баре\n\'!пить\' - выпить напиток\n'
        '@ Бармен:\n\'!принять <имя>\' - принять заказ```')


@bot.command(name='паспорт')
async def passport(ctx):
    data = open_db("database/passports.json")
    user = str(ctx.author)
    if user in data:
        money = data[user]["coin"]
        items = ''
        for item in data[user]["items"]:
            items = items + '```py\n@ ' + item + '\n' + '```'
        items = items if items != '' else '```py\n @ пусто```'
        await ctx.send('**Инвентарь ' + ctx.author.name + ':**\n' + items + '\nДеньги: ' + str(money) + ':pizza:')
    else:
        data[user] = {
            'coin': 0,
            'item': [],
            'work': False
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
                order[user_name] = ''
            order[user_name] = drink
            update_db("database/bar.json", data_bar)
            await ctx.send(ctx.author.name + ' заказал ' + drink)
            return
    menu = ''
    for drink_menu in drinks:
        drink_menu_str = str(drink_menu)
        menu = menu + drink_menu_str + ': ' + str(drinks[drink_menu_str]["cost"]) + ':pizza:' + '\n'
    await ctx.send(ctx.author.name + ': \n' + menu)


@bot.command(name='принять')
@commands.has_role("бармен")
async def drink_accept(ctx, user: discord.Member):
    data = open_db("database/passports.json")
    data_bar = open_db("database/bar.json")
    items = open_db("database/items.json")
    client = str(user)
    if client in data_bar["order"]:
        order = data_bar["order"][client]
        if data[client]["coin"] >= items["drinks"][str(order)]["cost"]:
            print(order)
            data[client]["coin"] -= items["drinks"][str(order)]["cost"]
            data[client]["items"].append(str(order))
            data[str(ctx.author)]["coin"] += items["drinks"][str(order)]["cost"]
            update_db('database/passports.json', data)
            order2 = data_bar["order"].pop(client)
            update_db('database/bar.json', data_bar)
            await ctx.send('Заказ ' + client + 'оформлен(' + str(order2) + ')')
        else:
            await ctx.send('У ' + client + ' не достаточно средств')
    else:
        await ctx.send('Пользователь ничего не заказывал (Стёпа - дэбил)')


@drink_accept.error
async def accept_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Вы не бармен')


@bot.command(name='пить')
async def have_drink(ctx, drink):
    data = open_db("database/passports.json")
    items = open_db("database/items.json")
    drinks = items["drinks"]
    user_name = str(ctx.author)
    inventory = data[user_name]["items"]
    if drink in drinks and drink in inventory:
        inventory.remove(drink)
        update_db("database/passports.json", data)
        await ctx.send(ctx.author.name + ' выпил ' + drink)
        return
    await ctx.send("У вас нет такого предмета или его нельзя пить")


@bot.command(name='работать')
@commands.has_role("рабочий")
async def drink_accept(ctx):
    user = str(ctx.author)
    data = open_db("database/passports.json")
    salary = 10
    if not data[user]["work"]:
        data[user]["work"] = True
        update_db("database/passports.json", data)
        await ctx.send(ctx.author.name + ' начал работать')
        await asyncio.sleep(5)
        data[user]["coin"] += salary
        await ctx.send(ctx.author.name + ' заработал ' + str(salary))
        data[user]["work"] = False
        update_db("database/passports.json", data)
    else:
        await ctx.send(ctx.author.name + ', ты уже работаешь')

bot.run(config_bot['token'])
