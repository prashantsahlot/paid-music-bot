from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL

@Client.on_chat_join_request((filters.group | filters.channel))
async def autoapprove(client: Client, message: ChatJoinRequest):
  if not await db.check_join_request(message.from_user.id, message.chat.id):
    await db.add_join_request(message.from_user.id, message.chat.id)

@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    await db.delete_all_join_requests()    
    await message.reply("<b>⚙ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")



@Client.on_message(filters.command("add_link") & filters.user(ADMINS))
async def changeauth(client, m):
    sts = await m.reply_text("please wait...")
    args = m.command[1:]
    if not args:
        return await sts.edit("You need to provide a chat id starting with -100")
    args = args[0]
    try:
        args = int(args)
    except:
        return await sts.edit("You need to provide a chat id starting with -100")
    bot_admin = await is_bot_admin(client, args)
    if not bot_admin:
        return await sts.edit(f"⚠️ Make sure this bot admin that channel\n\nMake @{temp.U_NAME} admin in given channel {args}")	
    await db.update_link({"_id": "auth_channel", "value": int(args)})
    return await sts.edit(f"Changed!")
    
@Client.on_message(filters.command("get_link") & filters.user(ADMINS))
async def get_link(client, m): 
    ch = AUTH_CHANNEL
    link = await db.get_link("auth_channel", ch)
    await m.reply_text(f'your {link}')	


@Client.on_message(filters.command("del_link") & filters.user(ADMINS))
async def del_link(client, m): 
    await db.delete_all_link()
    await m.reply_text('Deleted')


async def is_bot_admin(c, channel_id):
    if channel_id:
        try:
            await c.create_chat_invite_link(channel_id)
            return True
        except Exception as e:
            return
    return True
