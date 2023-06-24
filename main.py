import discord
import json


config = json.loads(open("config.json","r").read())
intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.message_content = True
intents.guild_messages = True

client = discord.Client(intents=intents)
def load_datas():
    return json.loads(open("data.json","r").read())

def dump_datas(new_datas):
    open("data.json","w").write(json.dumps(new_datas))
    

@client.event
async def on_ready():
    print(f'Successfull login : {client.user}')

def trackUser(user: discord.User | discord.Member,tracker_id):
    js = load_datas()
    for ur in js:
        if ur["id"] == user.id:
            ur["trackers"].append(user.id)
            return
    status_text = ""
    for a in user.activities:
        if isinstance(a, discord.CustomActivity):
            status_text = a.name
    roles = []
    for role in user.roles:
        print(role.name)
        roles.append(role.name)
    
    userData = {
        "name": user.display_name,
        "id": user.id,
        "avatar_url": user.display_avatar.url,
        "status": user.status.name,
        "status_text": status_text,
        "roles": roles,
        "trackers": [
            tracker_id
        ]
    }
    
    js.append(userData)
    
    dump_datas(js)
    
@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith('$track'):
        member = None
        for mem in message.guild.members:
            if mem.id == int(message.content.split(" ")[1]):
                member = mem
        if not member:
            await message.channel.send("User not found")
            return
        trackUser(member,message.author.id)
        await message.channel.send(message.author.name)

@client.event
async def on_member_update(before,user):
    jsall = load_datas()
    for mem in jsall:
        if mem["id"] == user.id:
            js = mem
    status_text = ""
    for a in user.activities:
        if isinstance(a, discord.CustomActivity):
            status_text = a.name
    roles = []
    for role in user.roles:
        print(role.name)
        roles.append(role.name)
    js["status_text"] = status_text
    js["roles"] = roles
    
    
    for i in range(len(jsall)):
        if jsall[i]["id"] == user.id:
            index = i
    for tracker in jsall[index]["trackers"]:
        async for guild in client.fetch_guilds():
            async for s in guild.fetch_members():
                if s.id == tracker:
                    await (await s.create_dm()).send(f"User {user.nick} updated !\n````{js}```")

    
    
    
    jsall[index] = js
    dump_datas(jsall)

client.run(config["token"])