# How to get tokens for this bot

## Discord token

To get a discord bot token you need to create a bot
Create one by heading to the [Discord Developer Portal](https://discord.com/developers/applications)

1. Click on New Application in the top right corner

 <img src=https://cdn.discordapp.com/attachments/917290615140667454/1006815657523949578/unknown.png width=120px>

2. Give it a name, this can be anything you want and click create

 <img src=https://cdn.discordapp.com/attachments/917290615140667454/1006816034583486544/unknown.png width=350px>

3. Go to the left side and click on Bot then click on Add bot

 <img src=https://cdn.discordapp.com/attachments/917290615140667454/1006816399462780979/unknown.png width=250px>
 <img src=https://cdn.discordapp.com/attachments/917290615140667454/1006816412351864912/unknown.png width=150px>

4. Click on reset token (if its not visible)

  <img src=https://cdn.discordapp.com/attachments/917290615140667454/1006817217490473020/unknown.png width=580px>

5. Copy the token and paste it into the .env file in the root directory

```
TOKEN=<token>
```

## Github Token

1. Go to the github token creation page [here](https://github.com/settings/tokens/new)

2. Select the repo scope
   <img src=https://cdn.discordapp.com/attachments/917290615140667454/1006818751250956348/unknown.png>

3. Click on Generate Token

 <img src=https://cdn.discordapp.com/attachments/917290615140667454/1006818754644164648/unknown.png width=150px>

4. Copy it and put it in your .env file!

```
...
GH_TOKEN=<github token>
```
