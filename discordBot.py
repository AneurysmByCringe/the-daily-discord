### "The Daily Discord", originally made by DatInnovator/AneurysmByCringe. ###
# Beware: noob coding ahead! Feel free to make suggestions, I get to learn more :)
# This bot utilizes free APIs to distribute weather and news information for your desired country/city.
# Weather API: OpenWeatherMap <https://openweathermap.org>
# News API: News API Developer by NewsAPI.org <https://newsapi.org>
# Licensed under the MIT License, 2019.

import discord
import requests
import json
from discord.ext import commands
from newsapi import NewsApiClient

bot = commands.Bot(command_prefix='$')
token = '<Discord Bot Token>'
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Logged in!')
    print(bot.user.name)
    print(bot.user.id)


@bot.command()
async def weather(ctx, arg):
    city_name = arg
    API_KEY = '<OpenWeatherMap API Key>'
    api = "http://api.openweathermap.org/data/2.5/forecast?units=metric&q={city}&APPID={key}"

    url = api.format(city=city_name, key=API_KEY)
    response = requests.get(url)
    js = response.json()

    embed = discord.Embed(title="Tomorrow's Forecast for " + city_name.upper(),
                          description="Weather for every 3 hours", color=0x027465)

    for dates in js["list"]:
        embed.add_field(name=dates['dt_txt'],
                        value="Temperature: {}\n{}".format(dates["main"]["temp"], dates["weather"][0]["description"]), inline=False)

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def news(ctx, arg, arg2):
    country = arg
    category = arg2
    newsAPIkey = '<News API Key>'
    apiurl = "https://newsapi.org/v2/top-headlines?country={countryCode}&category={catCode}&apiKey={apiKey}"

    url = apiurl.format(countryCode=arg, catCode=arg2, apiKey=newsAPIkey)
    response = requests.get(url)
    js = response.json()

    embed = discord.Embed(title="You requested " + arg2 + " news for " +
                          arg.upper(), description="Powered by NewsAPI.org", color=0x027465)

    for articles in js["articles"]:
        embed.add_field(name=articles["title"],
                        value=articles["url"], inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="The Daily Discord",
                          description="For that 1% of seriousness you need in Discord.", color=0x027465)

    embed.add_field(name="$weather <City Name>",
                    value="This will give you a 5 day, 3 hour forecast for the city.\nIf your city name contains a space, please use the '+' sign.'", inline=False)
    embed.add_field(name="$news <Country Code> <News Topic>",
                    value="This will give you a list of trending news for your country.\nThe country code is the 2-letter ISO 3166-1 code (some countries may not work), and the topics include general, entertainment, business, technology, etc.", inline=False)
    embed.add_field(name="$helpme", value="Gives this message.", inline=False)

    await ctx.send(embed=embed)


bot.run(token)
