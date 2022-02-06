from asyncio.windows_events import NULL
from distutils.util import change_root
from email import message, message_from_string
from operator import truediv
from pickle import FALSE, TRUE
import winreg
import discord
import os
import json
from re import search

TOKEN = 'ODkzNTY4OTQ4MDgyMjAwNjA4.YVdW7g.pysiQCuvQeuW7LmklaSs1-nJ0w4'
client = discord.Client()
global json_file_path
json_file_path = os.path.dirname(os.path.abspath(__file__)) +"\main.json"

global new_match
new_match = False
match_is_playing = False
player = ["",""]
global board
board = [0,0,0,
         0,0,0,
         0,0,0]
player_now =""


@client.event
async def on_ready():
    global match_is_playing
    match_is_playing = False
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
        global match_is_playing
        global new_match
        global player_now
        if user_message == "new game" and new_match == False and match_is_playing == False:
            await message.channel.send(f'new match ist starting (join with join)')
            new_match = True
            return
        elif user_message =="join" and new_match == True and match_is_playing == False:
            if player[0] == "":
                player[0] = username
                await message.channel.send(f'{username} joined')
            elif player[1] == "":
                player[1] = username
                await message.channel.send(f'{username} joined')

            if player[0] != "" and player[1] != "":
                match_is_playing = True
                await message.channel.send("1st player is " + player[0] + "(you place with place <Int between 0 and 8>)")
                player_now = player[0]
                await print_board(message)
            return
        elif search("place",user_message) and match_is_playing == True and match_is_playing == True:
            if username == player[0] and player_now == player[0]:
                if board[int(user_message[6])] == 0:
                    board[int(user_message[6])] = 8
                player_now = player[1]
                await print_board(message)
                await look_for_win(message) 
            elif username == player[1] and player_now == player[1]:
                if board[int(user_message[6])] == 0:
                    board[int(user_message[6])] = 4
                player_now = player[0]
                await print_board(message)
                await look_for_win(message)
        elif user_message == "cancel":
            await cancel(message)
        elif user_message == "user":
            await print_user(message, username) 
        elif user_message == "help":
            await message.channel.send("-new game\t -makes new game \n-join\t\t\t\t -you join an open game\n-place\t\t\t  -places your point at the a point\n-user\t\t\t\t-shows scores")

def look_for_ex(username):
    global json_file_path
    with open(json_file_path,"r") as json_file:
        data = json.load(json_file)
        for i in data["player"]:
            if i['name'] == username:
                return
    new_user(username)
    return


def new_user(username):
    new_player ={
            "name": username,
            "won": 0,
            "lost":0,
            "draw":0
        }

    with open(json_file_path,"r+") as json_file:
        file_data = json.load(json_file)
        file_data["player"].append(new_player)
        json_file.seek(0)
        json.dump(file_data, json_file, indent = 4)
    return

async def print_user(message_in, username):
    look_for_ex(username)
    global won
    won = 0
    global lost
    lost = 0
    global draw
    draw = 0

    with open(json_file_path,"r") as json_file:
        data = json.load(json_file)
        for i in data["player"]:
            if i['name'] == username:
                won = i['won']
                lost = i['lost']
                draw = i['draw']
                break
    await message_in.channel.send(f"macthes won {won} matches lost {lost} matches ended in a draw {draw}")
    return

async def add_score(messsage_in, winner):
    look_for_ex(player[winner])
    global loser 
    global change_1
    change_1 = NULL
    global change_2
    change_2 = NULL
    if winner == 0:
        change_1 = 'won'
        change_2 = 'lost'
        loser = 1
    elif winner == 1:
        change_1 = 'lost'
        change_2 = 'won'
        loser = 0
    elif winner == 2:
        change_1 = 'draw'
        change_2 = 'draw'
        winner = 0
        loser = 1
    with open(json_file_path,"r+") as json_file:
        data = json.load(json_file)
        for i in data["player"]:
            if i['name'] == player[winner]:
                i[change_1] = i[change_1]+1
                json_file.seek(0)
                json.dump(data, json_file, indent = 4)
                break 
    with open(json_file_path,"r+") as json_file:
        data = json.load(json_file)
        for i in data["player"]:
            if i['name'] == player[loser]:
                i[change_2] = i[change_2]+1
                json_file.seek(0)
                json.dump(data, json_file, indent = 4)
                break           
    return

async def look_for_win(message_in):
    #horizontal
    have_to_win_p1 = 0
    have_to_win_p2 = 0
    for x in range(3):
        for y in range(3):
            if board[y+x*3] == 8:
                have_to_win_p1 = have_to_win_p1 + 1
            elif board[x*y] == 4:
                have_to_win_p2 = have_to_win_p2 + 1
        if have_to_win_p1 == 3:
            await win(message_in,0)
        elif have_to_win_p2 == 3:
            await win(message_in,1)
        have_to_win_p1 = 0
        have_to_win_p2 = 0
    # vertical
    for x in range(3):
        for y in range(3):
            if board[x+y*3] == 8:
                have_to_win_p1 = have_to_win_p1 + 1
            elif board[x+y*3] == 4:
                have_to_win_p1 = have_to_win_p1 + 1
            if have_to_win_p1 == 3:
                await win(message_in,0)
            elif have_to_win_p2 == 3:
                await win(message_in,1)
        have_to_win_p1 = 0
        have_to_win_p2 = 0
    # other (yeah i know the word, do you?)  (Top right -> bottom left)
    if board[2] == 8 and board[4] == 8 and board[6] == 8:
        await win(message_in,0)
    elif board[2] == 4 and board[4] == 4 and board[6] == 4:
        await win(message_in,1)
    # other (yeah i know the word, do you?)  (Top left -> bottom right)
    if board[0] == 8 and board[4] == 8 and board[8] == 8:
        await win(message_in,0)
    elif board[0] == 4 and board[4] == 4 and board[8] == 4:
        await win(message_in,1)
    #look for draw / full board
    placed = 0
    for x in range(len(board)):
        if board[x] != 0:
            placed = placed +1
    if placed == 9:
        add_score(message,2)
    return


async def win(message_in,win):
    await message_in.channel.send(f"{player[win]} won")
    await add_score(message_in,win)
    await cancel(message_in)
    return

async def cancel(message_in):
    global match_is_playing
    global new_match
    global player_now
    await message_in.channel.send("game ended")
    player[0] = ""
    player[1] = ""
    for x in range(len(board)):
        board[x] = 0
    player_now = ""
    new_match = False
    match_is_playing = False
    return

async def print_board(new_message):    
    global print_string
    print_string = "" 
    for x in range(len(board)):
        if x%3==0:
            print_string += "\n"
        if board[x] == 8:
            print_string += ":x:"
        elif board[x] == 4:
            print_string += ":o:"
        else:
            print_string += ":white_square_button:"
    
    await new_message.channel.send(f"{print_string}")
    return

client.run(TOKEN)
