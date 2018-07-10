# Grabulous
A Discord py bot for Windows which downloads a channel's images. How convenient!

## Requirements

* [Python 3.4.2+](https://www.python.org/downloads/) with `pip`
    * The bot will NOT WORK with python 3.7.0. Use pyenv if needed (latest compatible version: 3.6.6).

## About the Bot

If you host active art channels and want to keep a steady archive of its creations, manually downloading images is a hassle. The "recommended" solution is to use self-botting tools, which is a violation of Discord's terms of service.

With Grabulous, every image uploaded to your server can be downloaded with a unique tag and ID, so you can focus on removing duplicates, categorizing images, and creating a more streamlined experience for anyone looking for certain creators or images.

Grabulous is a **self-hosted** bot; it only runs when you want it to, and it runs from your own computer.

## How to do it

### Part 1: Setting up project
1. Install Python!
2. Clone or download this repo and unzip `Grabulous-master` where you want
3. Run `pip install -r requirements.txt` to install dependencies
    * You can ignore the dependencies errors from `discord-py`, it works fine for now.

### Part 2: Setting up a Discord bot
4. [Create a Discord Bot, get an application token, and add the bot to your server](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
5. Create a file called `inf.py` and add the following line *followed by a line break*:
```python
def token(): return "Replace this text with your application token"
```

### Part 3: Customizing the config.cxr file
6. [Activate Developer Mode in Discord and copy your User ID](https://youtu.be/fqAwlX0c_Vc?t=6) (video, 20 seconds)
7. In `Grabulous-master`, open `config.cxr` in a text editor like Notepad++

Grabulous uses an easy-to-read markup language and loads/saves them as `.cxr` files. Items in these files look like this:
```
#key
/ Lines with a slash are ignored!
/ Tags and values are separated by a colon.
tag: value
other tag: other value
tag without value
```

You will be adding to these files

8. Paste your User ID under `#permissions` in place of the long string of 0s.
9. If there is a different folder or file path where you want images to download (such as a local Google Drive folder) then change the value of root under `#init` like so:
```
root: /path/to/download/location
```

### Part 4: Running the bot
10. Run the bot with `python grabulous.py`
11. In Discord, type one of the commands below to begin downloading images:
```
-grab                               downloads images from the channel which the command was posted in
-grab #channel                      downloads images from the tagged channel
-grab #channel1 #channel2 ...       downloads images from all tagged channels
```

### Part 5: Support this bot on (the original) Patreon!

If you appreciate what this bot does, consider pledging to the __upstream__ [Patreon](https://www.patreon.com/complexor)! Every bit makes a difference.
