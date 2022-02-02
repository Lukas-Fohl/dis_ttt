from asyncio.windows_events import NULL
from email import message, message_from_string
from operator import truediv
from pickle import FALSE, TRUE
import discord
from re import search

TOKEN = 'ODkzNTY4OTQ4MDgyMjAwNjA4.YVdW7g.CAmUPW_I32s8-F7rZ1PC9ztZ2w4'
client = discord.Client()

global new_match
new_match = False
match_is_playing = False
player = ["ab","cd"]
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
        if user_message == "new game" and new_match == False and match_is_playing == False:
            await message.channel.send(f'new match ist starting (join with join)')
            new_match = True
            return
        elif user_message =="join" and new_match == True and match_is_playing == False:
            if player[0] == "ab":
                player[0] = username
                await message.channel.send(f'{username} joined')
                print(username)
            elif player[1] == "cd":
                player[1] = username
                await message.channel.send(f'{username} joined')
                print(username)

            if player[0] != "ab" and player[1] != "cd":
                match_is_playing = True
                await message.channel.send("1st player is " + player[0] + "(you place with place <Int between 0 and 8>)")
                player_now = player[0]
                await print_board(message)
            return
        elif search("place",user_message) and match_is_playing == True and match_is_playing == True:
            if username == player[0] and player_now == player[0]:
                print(int(user_message[6]))
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
        elif user_message == "config":
            print()
        elif user_message == "help":
            await message.channel.send("-start game\t-makes new game \n-join\t\t\t\t -you join an open game\n-place\t\t\t  -places your point abt the a point")


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
        print()
        await win(message_in,0)
    elif board[2] == 4 and board[4] == 4 and board[6] == 4:
        print()
        await win(message_in,1)
    # other (yeah i know the word, do you?)  (Top left -> bottom right)
    if board[0] == 8 and board[4] == 8 and board[8] == 8:
        print()
        await win(message_in,0)
    elif board[0] == 4 and board[4] == 4 and board[8] == 4:
        print()
        await win(message_in,1)
    return

async def win(message_in,win):
    await message_in.channel.send(f"{player[win]} won")
    await cancel(message_in)
    return

async def cancel(message_in):
    global match_is_playing
    global new_match
    global player_now
    await message_in.channel.send("game ended")
    player[0] = "ab"
    player[1] = "cd"
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
