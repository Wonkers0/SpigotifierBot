import lightbulb
import hikari

bot = lightbulb.BotApp(token="[YOUR TOKEN HERE]")
FULL = "✅ Fully Supported"
PARTIAL = "⚠ Partially Supported"
NONE = "❌ Not Supported"

actionDict = {
  "SendMessage": FULL,
  "PlaySound": FULL,
  "SendTitle": FULL,
  "SetBossBar": FULL,
  "RemoveBossBar": FULL,
  "ActionBar": FULL,
  "SendMessageSeq": FULL,
  "PlaySoundSeq": FULL,
  "SendHover": FULL,
  "StopSound": FULL,
  "SetTabListInfo": FULL,
  "GiveItems": FULL,
  "SetHotbar": FULL,
  "SetInventory": FULL,
  "SetSlotItem": FULL,
  "SetEquipment": FULL,
  "SetArmor": FULL,
  "ReplaceItems": FULL,
  "RemoveItems": FULL,
  "ClearItems": FULL,
  "SetCursorItem": FULL,
  "ClearInv": FULL,
  "SetItemCooldown": FULL,
  "SaveInv": FULL,
  "LoadInv": FULL,
  "ShowInv": FULL,
  "ExpandInv": FULL,
  "SetMenuItem": FULL,
  "SetInvName": FULL,
  "CloseInv": FULL,
  "RemoveInvRow": FULL,
  "AddInvRow": FULL,
  "OpenBlockInv": FULL,
  "Damage": FULL,
  "Heal": FULL,
  "SetHealth": FULL,
  "SetMaxHealth": FULL,
  "SetAbsorption": FULL,
  "SetFoodLevel": FULL,
  "SetSaturation": FULL,
  "GiveExp": FULL,
  "Points": FULL,
  "Level": FULL,
  "Level": FULL,
  "SetExp": FULL,
  "Points": FULL,
  "Level": FULL,
  "Level": FULL,
  "GivePotion": FULL,
  "RemovePotion": FULL,
  "ClearPotions": FULL,
  "SetSlot": FULL,
  "SetAtkSpeed": FULL,
  "SetFireTicks": FULL,
  "SetFreezeTicks": FULL,
  "SetAirTicks": FULL,
  "SetInvulTicks": FULL,
  "SetFallDistance": FULL,
  "SetSpeed": FULL,
  "SetAllowFlight": FULL,
  "SetAllowPvP": FULL,
  "SetDropsEnabled": FULL,
  "SetInventoryKept": FULL,
  "SetCollidable": FULL,
  "InstantRespawn": FULL,
  "EnableBlocks": FULL,
  "DisableBlocks": FULL,
  "DisplayHologram": FULL,
  "IsSneaking": FULL,
  "IsSprinting": FULL,
  "IsGliding": FULL,
  "IsFlying": FULL,
  "IsGrounded": FULL,
  "IsSwimming": FULL,
  "IsBlocking": FULL,
  "IsLookingAt": FULL,
  "StandingOn": FULL,
  "IsNear": FULL,
  "InWorldBorder": FULL,
  "IsHolding": FULL,
  "HasItem": FULL,
  "IsWearing": FULL,
  "NoItemCooldown": FULL,
  "HasSlotItem": FULL,
  "MenuSlotEquals": FULL,
  "CursorItem": FULL,
  "NameEquals": FULL,
  "SlotEquals": FULL,
  "SwapHands": FULL,
  "Sneak": PARTIAL,
  "Leave": FULL,
  "Join": FULL,
  "=": FULL,
  "RandomValue": FULL,
  "PurgeVars": FULL,
  "+": FULL,
  "-": FULL,
  "x": FULL,
  "/": FULL,
  "%": FULL,
  "+=": FULL,
  "-=": FULL,
  "Exponent": FULL,
  "Root": FULL,
  "Logarithm": FULL,
  "ParseNumber": FULL,
  "AbsoluteValue": FULL,
  "ClampNumber": FULL,
  "WrapNumber": FULL,
  "Average": FULL,
  "RandomNumber": FULL,
  "Round": FULL,
  "Text": FULL,
  "ReplaceText": FULL,
  "RemoveText": FULL,
  "TrimText": FULL,
  "SplitText": FULL,
  "SetCase:": FULL,
  "TranslateColor": FULL,
  "TextLength": FULL,
  "RepeatText": FULL,
  "FormatTime": FULL,
  "CreateList": FULL,
  "AppendValue": FULL,
  "AppendList": FULL,
  "GetListValue": FULL,
  "SetListValue": FULL,
  "GetValueIndex": FULL,
  "ListLength": FULL,
  "=": FULL,
  "!=": FULL,
  ">": FULL,
  ">=": FULL,
  "<": FULL,
  "<=": FULL,
  "InRange": FULL,
  "LocIsNear": FULL,
  "Contains": FULL,
  "StartsWith": FULL,
  "EndsWith": FULL,
  "VarExists": FULL,
  "VarIsType": FULL,
  "ItemEquals": FULL,
  "ListContains": FULL,
  "ListValueEq": FULL,
  "SpawnMob": FULL,
  "SpawnItem": FULL,
  "SpawnVehicle": FULL,
  "SpawnExpOrb": FULL,
  "Explosion": FULL,
  "SpawnTNT": FULL,
  "SpawnFangs": FULL,
  "LeftClick": PARTIAL,
  "RightClick": PARTIAL
}

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
@lightbulb.add_checks(lightbulb.owner_only)
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

  await context.respond("```{result}```".format(result=result))


@bot.listen(lightbulb.CommandErrorEvent)
async def noPermEmbed(event):
  await event.context.respond(
      hikari.Embed(
      title="🔨 No Permission", 
      description="*You do not have permission to execute this command.*", 
      color=hikari.Color.from_hex_code("#cf1d1d")
      )
    )

bot.run()
