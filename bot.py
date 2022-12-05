import os
import lightbulb
import hikari
import miru
import json as jsonlib
import datetime
import re
from dotenv import load_dotenv

from actionparser import supportedActions, is_supported, parse_actions
from UserMenu import UserButton

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = lightbulb.BotApp(token=TOKEN)
err_color = hikari.Color.from_hex_code("#cf1d1d")
success_color = hikari.Color.from_hex_code('#76ff57')
date = datetime.datetime
request_date_format = "%m/%d/%Y, %H:%M %p"
miru.load(hikari.GatewayBot(TOKEN)) # Initialize miru library


@bot.command
@lightbulb.option("name", "The name of the action")
@lightbulb.command('issupported', 'Tells you if an action is supported or not.')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):
  if (len(context.options.name) >= 256):
    return await context.respond(hikari.Embed(title='😣 Invalid Input', description=f'There is no way that action exists anyway...\nLength: **{len(context.options.name)}/256**', color=hikari.Color.from_hex_code('#ff4747')))

  support_result = is_supported(str.lower(context.options.name))
  if(support_result != "NOT SUPPORTED"): 
    embed = hikari.Embed(title=context.options.name, description=f'✅ Found **{support_result}**', color=success_color)
  else:
    embed = hikari.Embed(title=context.options.name, description='❌ Could not find the action.', color=hikari.Color.from_hex_code('#ff4747'))

  await context.respond(embed)

@bot.command
@lightbulb.command('supportdump', 'Outputs a formatted version of all supported actions for use in supportdump.md')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):
  attachment = hikari.File(r"./action/supportdump.md");

  await context.respond(
      hikari.Embed(
        title="✅ Success!",
        description= "#️⃣ {amount} actions are currently supported.".format(amount=supportedActions),
        color=success_color
      ), attachment=attachment
    )

@bot.command
@lightbulb.command('about', 'About me')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):
  await context.respond(
      hikari.Embed(
        title="🤔 About this bot",
        description="This bot was created by Wonk#8781.\n\nThe point of this bot is to help you check if an action is supported or not.\nYou can use the `/issupported` command to check if an action is supported or not.\nYou can use the `/supportdump` command to output a file of all supported actions.\n\nSource code: https://github.com/Wonkers0/SpigotifierBot",
        color=success_color
      ),
    )

@bot.command
@lightbulb.option("name", "The name of the action you want to be added.")
@lightbulb.command('request', 'Request a new action to be supported.')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):
  action_name = str.lower(context.options.name)
  support_result = is_supported(action_name)
  userID = str(context.author.id)

  if(support_result != "NOT SUPPORTED"):
    await context.respond(
      hikari.Embed(
        title=f'✅ **{support_result}** is already supported.',
        description="You can check if an action is supported with `/issupported [action name]`",
        color=err_color
      )
    )
  else:
    with open('./action/actionrequests.json', "r", encoding='utf-8') as f:
      json_data = f.read()
    
    user_requests = jsonlib.loads(json_data)
    if(userID not in user_requests):
      user_requests[userID] =  init_request_profile(context.author.username)

    requests = user_requests[userID]["requests"]
    json = open('./action/actionrequests.json', 'w', encoding='utf-8')
    if(action_name in requests and getDateDiff(requests[action_name], request_date_format) <= 7):
      await context.respond(
        hikari.Embed(
          title="😵 You've already requested this action in the past week.",
          description="I'll try to get to it as soon as possible 🙏",
          color=err_color
        )
      )
      json.write(json_data)
    else:
      requests[action_name] = date.now().strftime(request_date_format)
      json.write(jsonlib.dumps(user_requests))

      await context.respond(
        hikari.Embed(
          title="📝 Submitted your request!",
          description="I'll try to get to it as soon as possible 👍",
          color=success_color
        )
      )
    json.close()

def init_request_profile(profileName):
  print("Initializing user profile...")
  return {
    "name": profileName,
    "requests": {}
  }


@bot.command
@lightbulb.option("reparse", "Update what actions are supported locally", required=False)
# @lightbulb.decorators.add_cooldown(60, 1,lightbulb.buckets.Bucket(60, 1))
@lightbulb.command("updaterequests", "Remove any supported actions from the json file")
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):
  if context.options.reparse:
    parse_actions()
  update_reqs()
  
  await context.respond(
    hikari.Embed(
      title="🔃 Done!",
      description="Updated all requests throughout all servers",
      color=success_color
    )
  )
  

@bot.command
@lightbulb.option("name", "Name of the user whose requests you wish to view", required=False)
@lightbulb.command("viewrequests", "View your latest requests")
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):
    with open('./action/actionrequests.json', "r", encoding='utf-8') as f:
      json_data = jsonlib.loads(f.read())
    foundUser = context.author

    if context.options.name:
      foundUser = await getUserFromName(context, context.options.name)
      if foundUser == None:
        return

    userID = str(context.author.id) if not context.options.name else str(foundUser.id)
    userName = context.author.username if not context.options.name else foundUser.username
    if userID in json_data.keys():
      requests = json_data[userID]["requests"]

    msg = ""
    if(userID not in json_data.keys() or len(requests.keys()) == 0):
      await context.respond(
        hikari.Embed(
          title=f"🔍 {userName} has no requests.", 
          description="*You can make a request using `/request [action name]`*", 
          color=err_color
        )
      )
      return
    
    print(requests)
    keys = list(requests.keys())
    start = len(requests) - 6 if len(requests) >= 6 else 0
    for i in range(start, len(requests)):
      diff = getDateDiff(requests[keys[i]], request_date_format)
      msg += f"**{keys[i]}**\nRequested at {requests[keys[i]]} *({diff + ' days' if diff > 0 else 'less than a day'} ago)*\n\n\n"

    await context.respond(
      hikari.Embed(
        title=f"{userName}'s Requests",
        description=msg,
        color=success_color
      ).set_thumbnail(foundUser.avatar_url)
    )
    
def getDateDiff(oldDate, date_format): # 'oldDate' should be a string formatted as a date
  return date.now().day - date.strptime(oldDate,  date_format).day
  
  
async def getUserFromName(context, name):
  foundUsers = []
  exactName = re.match("#\d{4}$", name) != None

  members = await context.bot.rest.fetch_members(context.guild_id)
  for user in members:
    if(not exactName and user.username == name):
      foundUsers.append(user)
    elif exactName:
      if(user.username + user.discriminator == name):
        return user

  if len(foundUsers) == 0:
    return None
  
  if len(foundUsers) > 5:
    await context.respond(
      hikari.Embed(
        title="🔢 Too many users with this name!",
        description= '\n'.join(foundUsers) + "\n\nTry adding a discriminator at the end, e.g. `foo#1234`",
        color=err_color
      )
    )
    return None
  elif len(foundUsers) > 1:
    view = miru.View()
    for user in foundUsers:
      print("Adding user: " + user.username + "#" + user.discriminator)
      view.add_item(UserButton(user.username + "#" + user.discriminator))
    
    message = await context.respond(
      hikari.Embed(
        title="👨‍👩‍👦‍👦 Found 2 or more users with the same name",
        description="Which one were you referring to?",
        color=hikari.Color.from_hex_code('#2d2f34')
      ), components=view.build()
    )

    view.start(await message.message())
    await view.wait()

    return None
  else:
    return foundUsers[0]

@bot.listen(lightbulb.CommandErrorEvent)
async def catch_errors(event):
  if(isinstance(event.exception, lightbulb.NotOwner)):
    await event.context.respond(
        hikari.Embed(
        title="🔨 No Permission", 
        description="*You do not have permission to execute this command.*", 
        color=err_color
        )
      )
  else:
    await event.context.respond(
      hikari.Embed(
        title="🔥 Waht?!",
        description="An internal error occurred :face_holding_back_tears:",
        color = err_color
      )
    )
    raise event.exception

@bot.listen(hikari.GuildMessageCreateEvent)
async def messageSent(event):
  contributors = [711657398724722708, 916875577015799818, 577082051895754782]
  if event.content == None:
    return

  if(event.author_id == 545012151081893898 and "<@1004187679493214219>" in event.content):
    await bot.rest.create_message(event.channel_id, hikari.Embed(title="🤩 Hey creator!", description="You are so unbelievably awesome.", color = hikari.Color.from_hex_code("#ff9933")), reply=event.message_id)
  if(event.author_id in contributors and "<@1004187679493214219>" in event.content):
    await bot.rest.create_message(event.channel_id, hikari.Embed(title="🎉 Hey contributor!", description="Thanks for working on me.", color = hikari.Color.from_hex_code("#ff6699")), reply=event.message_id)

def update_reqs():
    with open('./action/actionrequests.json', "r", encoding='utf-8') as f:
      json_data = jsonlib.loads(f.read())
    
    for profile in json_data.keys():
      requests = json_data[profile]["requests"]
      for request in requests.keys():
        if is_supported(request):
          del requests[request]

bot.run()
update_reqs() # Update requests on start-up
