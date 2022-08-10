# SpigotifierBot

Discord bot for the [DF Spigotifier](https://github.com/Wonkers0/DFSpigot) discord server

# How to run

1. Clone the repository and open the terminal, then type:

    `pip install -r requirements.txt`

    _(make sure you have pip installed and that you are in the correct directory)_

2. Make a `.env` file and in it type:

    ```
    TOKEN=<your bot token>
    GH_TOKEN=<your github token>
    ```

    _(If you don't know how to make a discord bot read [this](https://github.com/Wonkers0/SpigotifierBot/blob/main/TOKENS.md#discord-token))_

    _(If you don't know how to get a github token read [this](https://github.com/Wonkers0/SpigotifierBot/blob/main/TOKENS.md#github-token))_

3. Run the bot with:

    `py bot.py`

4. You should see that the bot is online and ready to go.

**Never share your .env file!!**

# Dev information

If you added a new library and you dont know how requirement.txt works, you can run

```
pip install pipreqs
pipreqs --encoding utf-8 .
```

_(Make sure you are in the correct directory)_
