from discord.ext.commands import Bot
from qoid import Qoid, Index
import requests
import os

print("#####################")
print("# Grabulous.discord #")
print("#     by Conrad     #")
print("######################")

cfg = Index.open(os.getcwd() + "\\config.cxr")
grab = Bot(command_prefix=cfg["init"]["pre"])
grab.remove_command("help")

if not cfg["init"]["root"]:
    cfg["init"]["root"] = ("root", os.getcwd())


# Decorator beneath Client.command()
def check(f):

    # Command wrapper which ensures permission and verifies
    async def wrap(ctx, *args):
        if ctx.message.author.id in cfg["permission"]:
            await grab.add_reaction(ctx.message, '✅')
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
                # with open(cfg["init"]["root"] + "\\" + msg.channel.name + "\\" + fn, 'wb') as handler:
                with open(f"{loc}\\{fn}", "ab") as handler:
                    handler.write(img_data)
                    print("Downloaded {0} to {1}\\{2}".format(e["url"], loc, fn))

                # cfg["init"].set(index=cfg["init"].index("failsafe"), this=Property("failsafe", msg.id))
                cfg[msg.channel.id]["failsafe"] = msg.id
                cfg.save(echo=False)


@grab.command(name="grab", pass_context=True)
@check
async def grabulate(ctx, *args):
    # Step 0: 
    wrap = None
    if args:
        wrap = args[0]
    else:
        wrap = ctx.message.channel.id

    # Step 1: Guarantee parameter submission is appropriate
    if wrap.startswith("<#") and wrap.endswith(">"):
        ch = grab.get_channel(wrap[2:-1])
    else:
        ch = grab.get_channel(wrap)
    if ch is None:
        await grab.say(f"Invalid channel {wrap} given")
        return

    # Step 2: Guarantee presence in config file
    if ch.id not in cfg:
        cfg.append(Qoid(ch.id, cfg["template"].val))
        cfg[ch.id]["server"] = ch.server.name
        cfg[ch.id]["name"] = ch.name
        cfg.save()

    # Step 3: Ensure directory exists
    msg = ctx.message
    serv = grab.get_server(ch.server.id)
    loc = None
    root = f"{cfg['init']['root']}\\{serv.name} ({serv.id})"
    ch_folder = f"{ch.name} ({ch.id})"
    if not os.path.isdir(f"{root}\\{ch_folder}"):
        try:
            if not os.path.isdir(root):
                os.mkdir(root)
            os.mkdir(f"{root}\\{ch_folder}")
            loc = f"{root}\\{ch_folder}"
        except FileExistsError:
            if not os.path.isdir(root):
                os.mkdir(f"{root}")
            os.mkdir(f"{root}_discord_downloads\\{ch_folder}")
            loc = f"{root}\\{ch_folder}_discord_downloads"
    else:
        loc = f"{root}\\{ch_folder}"

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
        af = None

    # Step 4: Traverse logs for
    print("Searching for image attachments...")
    end = False
    while not end:
        prev = bf
        async for msg in grab.logs_from(channel=ch, limit=100, before=bf, after=af):
            if msg.author.id != cfg["init"]["bot"]:
                await scrape_img(msg, loc)
            bf = msg
        if prev == bf:
            end = True
    print("All downloading complete.")
    # cfg["init"].set(index=cfg["init"].index("bookmark"), this=Property("bookmark", new_bookmark))
    cfg[ch.id]["bookmark"] = new_bookmark
    # cfg["init"].set(index=cfg["init"].index("failsafe"), this=Property("failsafe", ""))
    cfg[ch.id]["failsafe"] = None
    cfg.save(echo=False)
    print("Bookmark set to {0}".format(new_bookmark))


print("Initializing Sheo in {0}".format(cfg["init"]["root"]))

grab.run(cfg["init"]["token"])
