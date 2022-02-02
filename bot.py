from operator import truediv
from pickle import FALSE, TRUE
import discord
from re import search
import numpy as np

TOKEN = 'QmQ4XCpkPnOEthIQmDBDyqk7FSDdZGf3'

client = discord.Client()
global new_match
new_match = False
match_is_playing = False
player = ["ab","cd"]
global board
board = [0,0,0,
         0,0,0,
         0,0,0]
player_now ="";

@client.event
async def on_ready():
    global match_is_playing
    match_is_playing = False
    print('I\'m {0.user}'.format(client))
    game = discord.Game("nicht genshin impact")
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
        print(match_is_playing)
        if user_message == "!new game":
            await message.channel.send(f'new match ist starting (join with !join)')
            new_match = True
            return
        elif user_message =="!join" and new_match == True:
            if player[0] == "ab":
                player[0] = username
                print(username)
            elif player[1] == "cd":
                player[1] = username
                print(username)

            if player[0] != "ab" and player[1] != "cd":
                match_is_playing = True
                await message.channel.send("1st play is " + player[0])
                player_now = player[0]
                await print_board(message)
            return
        elif search("!place",user_message) and match_is_playing == True:
            if username == player[0] and player_now == player[0]:
                print(int(user_message[7]))
                if board[int(user_message[7])] == 0:
                    board[int(user_message[7])] = 8
                player_now = player[1]
                await print_board(message) 
            elif username == player[1] and player_now == player[1]:
                if board[int(user_message[7])] == 0:
                    board[int(user_message[7])] = 4
                player_now = player[0]
                await print_board(message)
        elif user_message == "cancel":
            cancel(message)

async def print_board(message_in):
    await message_in.channel.send(f"{board[0]}|{board[1]}|{board[2]}\n{board[3]}|{board[4]}|{board[5]}\n{board[6]}|{board[7]}|{board[8]}")
    return

async def look_for_win(message_in):
    #horizontal
    have_to_win_p1 = 0
    have_to_win_p2 = 0
    for x in range(3):
        for y in range(3):
            if board[x*y] == 8:
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
            if board[x+y*3-3] == 8:
                have_to_win_p1 = have_to_win_p1 + 1
            elif board[x+y*3-3] == 4:
                have_to_win_p1 = have_to_win_p1 + 1
            if have_to_win_p1 == 3:
                await win(message_in,0)
            elif have_to_win_p2 == 3:
                await win(message_in,1)
        have_to_win_p1 = 0
        have_to_win_p2 = 0
    # other (yeah i know the word, do you?)  (Top left -> bottom right)
    for x in range(3):
        if board[x*x] == 8:
            have_to_win_p1 = have_to_win_p1 + 1
        elif board[x*x] == 4:
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
    return

async def win(message_in,win):
    await message_in.channel.send(f"{player[win]} won")
    return

async def cancel(message_in):
    await message_in.channel.send("game ended")
    player[0] = ""
    player[1] = ""
    for x in range(len(board)):
        board[x] = 0
    player_now = "";
    new_match = False
    match_is_playing = False
    return

client.run(TOKEN)
