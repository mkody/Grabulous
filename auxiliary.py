import discord


async def discord_sanitize_arguments(client, ctx_ch, *args):
    """
    Convert valid discord ID numbers into messages

    :param client: the discord.Client which will retrieve info from the API
    :param ctx_ch: the channel in which the command was executed
    :param args: the original arguments passed in the message
    :return: the
    """
    out = []
    for a in args:
        # Test argument for Server
        serv_a = client.get_server(a)
        if serv_a:
            try:
                out.append(await serv_a)
                continue
            except discord.errors.HTTPException:
                pass

        # Test argument for Channel
        ch_a = client.get_channel(a[2:-1] if a.startswith("<#") and a.endswith(">") else a)
        if ch_a:
            out.append(ch_a)
            continue

        # Test argument for Message
        msg_a = client.get_message(ctx_ch, a)
        if msg_a:
            try:
                out.append(await msg_a)
                continue
            except discord.errors.HTTPException:
                pass

        # Test argument for User
        if a.startswith(("<@", "<@!")) and a.endswith(">"):
            i = 2 if a.startswith("<@") else 3
            usr_a = client.get_user_info(a[i:-1])
            if usr_a:
                try:
                    out.append(await usr_a)
                    continue
                except discord.errors.HTTPException:
                    pass
        out.append(a)
    return tuple(out)
