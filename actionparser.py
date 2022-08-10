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
actionInfo = {
  "actions": {},
  "allActions": [],
  "events": []
}

print("Parsing Actions")
# Get everything from github

repo = g.get_repo('Wonkers0/DFSpigot')

for file in repo.get_contents('utilities/actions'):
  name = file.name.replace('.java', '')
  actionInfo['actions'][name] = []
  content = b64decode(file.content).decode('utf-8')
  query = r'(?<=\n\t{4}case ").+(?=": {)'
  if(name.startswith('If')): query = r'(?<=\n\t{3}case ").+(?=": {)'
  for action in findall(query, content):
    actionInfo['actions'][name].append(action)
    actionInfo['allActions'].append(action)

for event in findall(r'(?<=\s\s)[A-Z]\w+(?=: \[.*\])', b64decode(repo.get_contents('website/script.js').content).decode('utf-8')):
  actionInfo['events'].append(event)


# Write to a markdown file

output = '''# Actions Support Dump
This lists all actions mentioned in DFSpigot source code.

## Actions'''

for actionCategory in actionInfo['actions']:
  output += '\n### ' + actionCategory + '\n'
  for action in actionInfo['actions'][actionCategory]:
    output += '* ' + action + '\n'

output += '\n## Events\n'

for event in actionInfo['events']:
  output += '* ' + event + '\n'

# Export everything to files
## Create the action directory
makedirs('action', exist_ok=True)

md = open('./action/supportdump.md', 'w+', encoding='utf-8')
md.write(output)
md.close()

json = open('./action/supportdump.json', 'w+', encoding='utf-8')
json.write(dumps(actionInfo))
json.close()

print("Parsing Actions Complete")