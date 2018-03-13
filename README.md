# Grabulous
A Discord py bot for Windows which downloads a channel's images. How convenient!

### Requirements
* [Python 3.4.2+](https://www.python.org/downloads/)
* [aiohttp](https://github.com/aio-libs/aiohttp/releases/latest)
* [async_timeout](https://github.com/aio-libs/async-timeout/releases/latest)
* [chardet](https://github.com/chardet/chardet/releases/latest)
* [discord.py](https://github.com/Rapptz/discord.py/releases/tag/v0.16.12)
* [multidict](https://github.com/aio-libs/multidict/releases/latest)
* qoid.py (a stable version is included in this repo)
* [requests](https://pypi.python.org/pypi/requests#downloads)
* [websockets](https://github.com/Lawouach/WebSocket-for-Python/releases/tag/0.4.2)

## About the Bot

If you host active art channels and want to keep a steady archive of its creations, manually downloading images is a hassle. The "recommended" solution is to use self-botting tools, which is a violation of Discord's terms of service.

With Grabulous, every image uploaded to your server can be downloaded with a unique tag and ID, so you can focus on removing duplicates, categorizing images, and creating a more streamlined experience for anyone looking for certain creators or images.

Grabulous is a **self-hosted** bot; it only runs when you want it to, and it runs from your own computer.

## How to do it

### Part 1: Setting up Python
0. Install Python!
1. Download this repo and unzip `Grabulous-master` where you want
2. Create a folder called `!python` inside `Grabulous-master`
3. Download and unzip the rest of the requirements into `!python`

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
root: C:\path\to\download\location
```

### Part 4: Running the bot
10. Open `!start_grab.bat`
11. In Discord, type one of the commands below to begin downloading images:
```

-grab                               downloads images from the channel which the command was posted in
-grab #channel                      downloads images from the tagged channel
-grab #channel1 #channel2 ...       downloads images from all tagged channels

### Part 5: Support this bot on Patreon!

If you appreciate what this bot does, consider pledging to my [Patreon](https://www.patreon.com/complexor)! Every bit makes a difference.
