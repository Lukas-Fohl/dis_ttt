from doctest import REPORT_UDIFF
import re
import discord
import os
import json
from re import search
import single_game as game
from multiprocessing import Process

TOKEN = ''
client = discord.Client()
global json_file_path
json_file_path_main = os.path.dirname(os.path.abspath(__file__)) +"\main.json"
json_file_path_id = os.path.dirname(os.path.abspath(__file__)) +"\game_id.json"


@client.event
async def on_ready():
    set_up_ids()
    print('I\'m {0.user}'.format(client))
    game = discord.Game("TicTacToe")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str (message.content)
    channel = str(message.channel.name)
    print(f'{username} : {user_message} (in: {channel})')

    if message.author == client.user:
        return
    if channel == 'ttt':
        if user_message == "new game":
            game.start_game = find_free_id()
            return
        elif user_message == "clear all games":
            clear_all_ids
            return

def clear_all_ids():
    end_all_games()
    return

def set_up_ids():
    global new_id
    for x in range(100):
        new_id ={"id":x,"used":False}
        with open(json_file_path_id,"r+") as json_file:
            file_data = json.load(json_file)
            file_data["ids"].append(new_id)
            json_file.seek(0)
            json.dump(file_data, json_file, indent = 4)
    return

def end_all_games():
    return

def find_free_id():
    for x in range(100):
        with open(json_file_path_id,"r+") as json_file:
            file_data = json.load(json_file)
            for i in file_data["ids"]:
                if i["used"] == False:
                    return i["id"]

client.run(TOKEN)