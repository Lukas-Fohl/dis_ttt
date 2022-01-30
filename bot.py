from operator import truediv
from pickle import FALSE, TRUE
import discord

TOKEN = 'ODkzNTY4OTQ4MDgyMjAwNjA4.YVdW7g.pqcrwdGPq6s9mFtbn1H_hN6sxzE'

client = discord.Client()
new_match = FALSE
match_is_playing = FALSE
player = {"",""}
board = {0,0,0,
         0,0,0,
         0,0,0};
global player_now
player_now ="";

@client.event
async def on_ready():
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
    if channel != 'TTT':
        global new_match
        if user_message == "!new game":
            await message.channel.send(f'new match ist starting (join with !join)')
            new_match = TRUE
            return
        elif user_message =="!join" & new_match == TRUE:
            if player[0] == "":
                player[0] = username
            elif player[1] == "":
                    player[1] = username
            if player[0] != "" & player[1] != "":
                match_is_playing = True
                await message.channel.send(f"1st play is {player[0]}")
                player_now = player[0]
                print_board(message)
            return
        elif "!place" in user_message:
            if username == player[0] & player_now == player[0]:
                player[user_message[7]] = 1
                player_now = player[1]
                print_board(message) 
            elif username == player[1] & player_now == player[1]:
                player[user_message[7]] = 2
                player_now = player[0]
                print_board(message)
        elif user_message == "cancel":
            player[0] = ""
            player[1] = ""
            for x in range(len(board)):
                board[x] = 0
            player_now = "";
            new_match = FALSE
            match_is_playing = FALSE

async def print_board(message_in):
    await message_in.channel.send(f"{board[0]}|{board[1]}|{board[2]}\n-----{board[3]}|{board[4]}|{board[5]}\n-----{board[6]}|{board[7]}|{board[8]}")
    return

async def look_for_win():
    return

client.run(TOKEN)
