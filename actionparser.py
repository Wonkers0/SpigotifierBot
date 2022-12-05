from os import makedirs
import os
from github import Github
from re import findall
# from dotenv import load_dotenv
#
# load_dotenv()
#
## it is expected this is run in a place with enviroment variables already loaded

TOKEN = os.getenv("GH_TOKEN")
g = Github(TOKEN)
actionInfo = {}
supportedActions = 0
all_actions = []

def parse_actions():
  print("Parsing Actions")
  # Get everything from github
  repo = g.get_repo('Wonkers0/DFSpigot')

  actionparams = repo.get_contents("DONT IMPORT/actionparams.json").decoded_content.decode('utf-8')

  matches = findall('"(.*?)": \[', actionparams)
  for match in matches:
    split = match.split(":")
    if(len(split) == 1):
      continue
    if(split[0] not in actionInfo.keys()):
      actionInfo[split[0]] = []

    supportedActions += 1
    actionInfo[split[0]].append("* " + split[1])
    all_actions.append(split[1])

  # Export everything to files
  ## Create the action directory
  makedirs('action', exist_ok=True)

  md = open('./action/supportdump.md', 'w+', encoding='utf-8')
  dump = "# Actions Support Dump\nThis lists all actions mentioned in actionparams.json"
  for key in actionInfo.keys():
    dump += "\n\n## " + key + "\n\n"
    dump += "\n".join(actionInfo[key])
  md.write(dump)
  md.close()

  json = open('./action/supportdump.json', 'w+', encoding='utf-8')
  json.write(actionparams)
  json.close()

  print("Parsing Actions Complete")

def is_supported(action_name):
  mapping = []
  for action in all_actions:
    mapping.append(str.lower(action))

  action_name = str.lower(action_name)
  if(action_name in mapping):
    return all_actions[mapping.index(action_name)]
  else:
    return "NOT SUPPORTED"
