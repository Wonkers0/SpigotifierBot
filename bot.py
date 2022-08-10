import os
import lightbulb
import hikari
from dotenv import load_dotenv

from actionparser import actionInfo
action_list = actionInfo['allActions'] + actionInfo['events']

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = lightbulb.BotApp(token=TOKEN)

@bot.command
@lightbulb.option("name", "The name of the action")
@lightbulb.command('issupported', 'Tells you if an action is supported or not.')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):
  if (len(context.options.name) >= 256):
    return await context.respond(hikari.Embed(title='😣 Invalid Input', description=f'There is no way that action exists anyway...\nLength: **{len(context.options.name)}/256**', color=hikari.Color.from_hex_code('#ff4747')))
  mapping = []
  for action in action_list:
    mapping.append(str.lower(action))
    mapping.append(action)
  all_actions = dict(zip(i := iter(mapping), i))

  action_name = str.lower(context.options.name)
  if(action_name in all_actions): 
    embed = hikari.Embed(title=context.options.name, description=f'✅ Suported **{all_actions[action_name]}**', color=hikari.Color.from_hex_code('#76ff57'))
  else:
    embed = hikari.Embed(title=context.options.name, description='❌ Unsupported', color=hikari.Color.from_hex_code('#ff4747'))

  await context.respond(embed)

@bot.command
@lightbulb.command('supportdump', 'Outputs a formatted version of all supported actions for use in supportdump.md')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):


  attachment = hikari.File(r"./action/supportdump.md");

  await context.respond(
      hikari.Embed(
        title="✅ Success!",
        description= "#️⃣ {amount} actions are currently supported.".format(amount=len(action_list)),
        color=hikari.Color.from_hex_code('#76ff57')
      ), attachment=attachment
    )

@bot.command
@lightbulb.command('about', 'About me')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(context):
  await context.respond(
      hikari.Embed(
        title="🤔 About this bot",
        description= "This bot was created by Wonk#8781.\n\nThe point of this bot is to help you check if an action is supported or not.\nYou can use the `/issupported` command to check if an action is supported or not.\nYou can use the `/supportdump` command to output a file of all supported actions.\n\nSource code: https://github.com/Wonkers0/SpigotifierBot",
        color=hikari.Color.from_hex_code('#76ff57')
      ),
    )



@bot.listen(lightbulb.CommandErrorEvent)
async def catch_errors(event):
  err_color = hikari.Color.from_hex_code("#cf1d1d")

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
        description="An internal error occurred 😭",
        color = err_color
      )
    )
    raise event.exception

bot.run()
