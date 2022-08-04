import os
import lightbulb
import hikari
from dotenv import load_dotenv

from actionDict import actionDict, FULL, PARTIAL, NONE

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = lightbulb.BotApp(token=TOKEN)

@bot.command
@lightbulb.option("name", "The name of the action")
@lightbulb.command('issupported', 'Tells you if an action is supported or not.')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):
  actionName = str.lower(context.options.name)

  insensitiveDict = dict((k.lower(), v) for k, v in actionDict.items()) 

  global actionSupport, color, displayName
  if(actionName in insensitiveDict): 
    actionSupport = insensitiveDict.get(actionName)
    displayName = list(actionDict.keys())[list(insensitiveDict.keys()).index(actionName)]
  else:
    actionSupport = NONE
    displayName = context.options.name
     
  if(actionSupport == FULL): color = hikari.Color.from_hex_code('#76ff57')
  elif(actionSupport == PARTIAL): color = hikari.Color.from_hex_code('#ff8f4a')
  elif(actionSupport == NONE): color = hikari.Color.from_hex_code('#ff4747')

  embed = hikari.Embed(title=displayName, description=actionSupport, color=color)
  await context.respond(embed)

@bot.command
@lightbulb.command('supportdump', 'Outputs a formatted version of all supported actions for use in supported_actions.md')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):
  actions = list(actionDict.keys())
  result = ""
  
  for action in actions:
    global prefix
    if(actionDict.get(action) == FULL): prefix = "✅"
    elif(actionDict.get(action) == PARTIAL): prefix = "⚠"
    result += "{prefix} {action}\n\n".format(action=action, prefix=prefix)

  f = open("supportdump.txt","w+", encoding="utf-8")
  f.write(result)
  f.close()

  attachment = hikari.File(r"C:\Users\David\Desktop\Discord Bot\supportdump.txt");

  await context.respond(
      hikari.Embed(
        title="✅ Success!",
        description= "#️⃣ {amount} actions are currently supported.".format(amount=len(actions)),
        color=hikari.Color.from_hex_code('#76ff57')
      ), attachment=attachment
    )



@bot.listen(lightbulb.CommandErrorEvent)
async def catchErrors(event):
  errColor = hikari.Color.from_hex_code("#cf1d1d")

  if(isinstance(event.exception, lightbulb.NotOwner)):
    await event.context.respond(
        hikari.Embed(
        title="🔨 No Permission", 
        description="*You do not have permission to execute this command.*", 
        color=errColor
        )
      )
  else:
    await event.context.respond(
      hikari.Embed(
        title="🔥 Waht?!",
        description="An internal error occurred 😭",
        color = errColor
      )
    )
    raise event.exception

bot.run()
