from base64 import b64decode
from json import dumps
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
actionInfo = []

print("Parsing Actions")
# Get everything from github

repo = g.get_repo('Wonkers0/DFSpigot')

actionparams = repo.get_contents("DONT IMPORT/actionparams.json").decoded_content.decode('utf-8')
matches = findall('"(.*?)": \[', actionparams)
for match in matches:
  if(len(match.split(":")) == 1):
    continue
  actionInfo.append(match.split(":")[1])

# Export everything to files
## Create the action directory
makedirs('action', exist_ok=True)

md = open('./action/supportdump.md', 'w+', encoding='utf-8')
md.write("\n".join(actionInfo))
md.close()

json = open('./action/supportdump.json', 'w+', encoding='utf-8')
json.write(actionparams)
json.close()

print("Parsing Actions Complete")
