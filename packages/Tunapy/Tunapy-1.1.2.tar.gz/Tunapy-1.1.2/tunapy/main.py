from python_imagesearch.imagesearch import imagesearch_loop
import discord
import os
from dotenv import load_dotenv
from itertools import cycle
from pagerIncidents import trigger_incident


link="https://discord.com/oauth2/authorize?client_id=797364395185143818&scope=bot&permissions=2147483647"

load_dotenv()
client = discord.Client()
token = os.getenv("bot_token")

status = cycle(['BdmBrs | !brs', 'House'])
prefix = "!"
initBrs = "brsTrack"
initHotTime = "hotTimeTrack"
startTracking = False

@client.event
async def on_ready():
    msg = "{0} is logged on.".format(client.user.display_name)
    print(msg)
    await client.change_presence(activity=discord.Game(next(status)))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    cmd = message.content.lower()
    author = message.author
    channel = message.channel
    if len(cmd) > 0:
        get_prefix = cmd[0]
        if prefix == get_prefix:
            cmd = cmd[1:]
            if cmd == initBrs.lower():
                msg="<@{0}>, Brs has been spotted in Heidel".format(author.id)
                pos = imagesearch_loop("./brs.png", 1)
                if pos[0] != -1:
                    print("position : ", pos[0], pos[1])
                    trigger_incident()
                    return await channel.send(msg)
            elif cmd == initHotTime.lower():
                pos = imagesearch_loop("./ht1.png", 1)
                msg="<@{0}>, Hot time has been activated in Heidel".format(author.id)
                if pos[0] != -1:
                    print("position : ", pos[0], pos[1])
                    #trigger_incident()
                    return await channel.send(msg)
            else:
                msg="<@{0}>, That's an invalid command".format(author.id)
                return await channel.send(msg)
                
                

if __name__ == "__main__":
    client.run(token)