from discord.ext.commands import Bot
from discord import Channel
from qoid import Qoid, Index
from auxiliary import discord_sanitize_arguments as sanitize
import datetime
import requests
import os
from inf import token

print("#####################")
print("# Grabulous.discord #")
print("#     by Conrad     #")
print("#   edits by Kody   #")
print("#####################")
print()

cfg = Index.open(os.getcwd() + "/config.cxr")
grab = Bot(command_prefix=cfg["init"]["pre"])
grab.remove_command("help")

if not cfg["init"]["root"]:
    cfg["init"]["root"] = ("root", os.getcwd())
    cfg.save()

if not os.path.isdir(cfg["init"]["root"]) and not os.path.isfile(cfg["init"]["root"]):
    os.mkdir(cfg["init"]["root"])
elif os.path.isfile(cfg["init"]["root"]):
    cfg["init"]["root"] = ("root", cfg["init"]["root"] + "-grabulous")
    os.mkdir(cfg["init"]["root"])
    cfg.save()


# Decorator beneath Client.command()
def check(f):

    # Command wrapper which ensures permission and verifies
    async def wrap(ctx, *args):
        if ctx.message.author.id in cfg["permission"]:
            await grab.add_reaction(ctx.message, '✅')
            args = await sanitize(grab, ctx, *args)
            await f(ctx, *args)
        else:
            print("Ignored illegal user!")
    return wrap


async def scrape_img(msg, loc):
    if msg.attachments:
        for e in msg.attachments:
            if e["url"].endswith(("png", "gif", "jpg")):
                img_data = requests.get(e["url"]).content
                sp = e["url"].split("/")
                fn = sp[len(sp) - 2] + "-" + sp[len(sp) - 1]
                with open(f"{loc}/{fn}", "ab") as handler:
                    handler.write(img_data)
                    print(f"Downloaded {e['url']} to {loc}/{fn}")
                cfg[msg.channel.id]["failsafe"] = msg.id
                cfg.save(echo=False)


@grab.event
async def on_ready():
    print("Ready to go!")


@grab.command(name="grab", pass_context=True)
@check
async def grabulate(ctx, *args):
    # Step 1: Get channels
    channels = [e for e in args if isinstance(e, Channel)]
    ids = []
    delete = []
    for e in channels:
        if e.id not in ids:
            ids.append(e.id)
        else:
            delete.append(e)
    ids = []
    for e in delete:
        channels.remove(e)
    # print([e.id for e in channels])

    if not channels:
        channels = [ctx.message.channel]

    for ch in channels:
        # Step 2: Guarantee presence in config file
        if ch.id not in cfg:
            cfg.append(Qoid(ch.id, cfg["template"].val))
            cfg[ch.id]["server"] = ch.server.name
            cfg[ch.id]["name"] = ch.name
            cfg.save()

        # Step 3: Ensure directory exists
        server = grab.get_server(ch.server.id)
        root = f"{cfg['init']['root']}/{server.name} ({server.id})"
        ch_folder = f"{ch.name} ({ch.id})"
        if not os.path.isdir(f"{root}/{ch_folder}"):
            try:
                if not os.path.isdir(root):
                    os.mkdir(root)
                os.mkdir(f"{root}/{ch_folder}")
                loc = f"{root}/{ch_folder}"
            except FileExistsError:
                if not os.path.isdir(root):
                    os.mkdir(f"{root}")
                os.mkdir(f"{root}_discord_downloads/{ch_folder}")
                loc = f"{root}/{ch_folder}_discord_downloads"
        else:
            loc = f"{root}/{ch_folder}"

        print(f"Beginning save in {root}")

        # Step 3: Establish start and end points for logs_from
        bf = None
        new_bookmark = None
        async for msg in grab.logs_from(channel=ch, limit=1):
            bf = new_bookmark = msg.id
            if cfg[ch.id]["failsafe"]:
                bf = cfg[ch.id]["failsafe"]
        if cfg[ch.id]["bookmark"]:
            af = await grab.get_message(channel=ch, id=cfg[ch.id]["bookmark"])
        else:
            af = datetime.datetime(2016, 1, 1)

        # Step 4: Traverse logs for
        print("Searching for image attachments...")
        end = False
        while not end:
            prev = bf
            async for msg in grab.logs_from(channel=ch, limit=100, before=bf, after=af):
                if msg.author.id != grab.user.id:
                    await scrape_img(msg, loc)
                bf = msg
            if prev == bf:
                end = True
        cfg[ch.id]["bookmark"] = new_bookmark
        cfg[ch.id]["failsafe"] = None
        cfg.save(echo=False)
        print(f"Bookmark set to {new_bookmark}")
    print(f"Downloading from {len(channels)} channel(s) complete.")


print(f"Initializing Grabulous in {cfg['init']['root']}")

grab.run(token())
