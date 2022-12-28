import os
import math
import json
import time
import shutil
import heroku3
import requests

from pyrogram import filters
from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from script import Script
from plugins.helpers import humanbytes
from database.filters_mdb import filter_stats
from database.users_mdb import add_user, find_user, all_users


@trojanz.on_message(filters.command('id') & (filters.private | filters.group))
async def showid(client, message):
    chat_type = message.chat.type

    if chat_type == "private":
        user_id = message.chat.id
        await message.reply_text(
            f"Your ID : `{user_id}`",
            parse_mode="md",
            quote=True
        )
    elif (chat_type == "group") or (chat_type == "supergroup"):
        user_id = message.from_user.id
        chat_id = message.chat.id
        if message.reply_to_message:
            reply_id = f"Replied User ID : `{message.reply_to_message.from_user.id}`"
        else:
            reply_id = ""
        await message.reply_text(
            f"Your ID : `{user_id}`\nThis Group ID : `{chat_id}`\n\n{reply_id}",
            parse_mode="md",
            quote=True
        )   


@trojanz.on_message(filters.command('info') & (filters.private | filters.group))
async def showinfo(client, message):
    try:
        cmd, id = message.text.split(" ", 1)
    except:
        id = False
        pass

    if id:
        if (len(id) == 10 or len(id) == 9):
            try:
                checkid = int(id)
            except:
                await message.reply_text("__Enter a valid USER ID__", quote=True, parse_mode="md")
                return
        else:
            await message.reply_text("__Enter a valid USER ID__", quote=True, parse_mode="md")
            return           

        if Config.SAVE_USER == "yes":
            name, username, dcid = await find_user(str(id))
        else:
            try:
                user = await client.get_users(int(id))
                name = str(user.first_name + (user.last_name or ""))
                username = user.username
                dcid = user.dc_id
            except:
                name = False
                pass

        if not name:
            await message.reply_text("__USER Details not found!!__", quote=True, parse_mode="md")
            return
    else:
        if message.reply_to_message:
            name = str(message.reply_to_message.from_user.first_name\
                    + (message.reply_to_message.from_user.last_name or ""))
            id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
            dcid = message.reply_to_message.from_user.dc_id
        else:
            name = str(message.from_user.first_name\
                    + (message.from_user.last_name or ""))
            id = message.from_user.id
            username = message.from_user.username
            dcid = message.from_user.dc_id
    
    if not str(username) == "None":
        user_name = f"@{username}"
    else:
        user_name = "none"

    await message.reply_text(
        f"<b>👨‍💼Name</b> : {name}\n\n"
        f"<b>📃User ID</b> : <code>{id}</code>\n\n"
        f"<b>👤Username</b> : {user_name}\n\n"
        f"<b>🔐Permanant USER link</b> : <a href='tg://user?id={id}'>Click here!</a>\n\n"
        f"<b>📑DC ID</b> : {dcid}\n\n",
        quote=True,
        parse_mode="html"
    )


@trojanz.on_message(filters.command('start') & filters.private)
async def start(client, message):
    await message.reply_text(
        text=Script.START_MSG.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                   InlineKeyboardButton("𝙲𝚘𝚖𝚖𝚊𝚗𝚍 𝙷𝚎𝚕𝚙", callback_data="help_data")
                ],
                [
                   InlineKeyboardButton("🗣️𝙶𝚛𝚘𝚞𝚙", url="https://t.me/Mo_tech_group"),
                   InlineKeyboardButton("🤖Bot List", url="https://t.me/Mo_Tech_YT/176"),
                   InlineKeyboardButton("👨‍💻Source", url="https://youtu.be/KrpqqNNLUSU")
                ],
                [
                   InlineKeyboardButton("🔻 Subscribe Now YouTube 🔻", url="https://youtu.be/KrpqqNNLUSU")
                ]
            ]
        ),
        reply_to_message_id=message.message_id
    )
    if Config.SAVE_USER == "yes":
        try:
            await add_user(
                str(message.from_user.id),
                str(message.from_user.username),
                str(message.from_user.first_name + " " + (message.from_user.last_name or "")),
                str(message.from_user.dc_id)
            )
        except:
            pass


@trojanz.on_message(filters.command('help') & filters.private)
async def help(client, message):
    await message.reply_text(
        text=Script.HELP_MSG,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🗣️𝙶𝚛𝚘𝚞𝚙", url="https://t.me/Mo_tech_group"),
                    InlineKeyboardButton("About Me👨‍💼", callback_data="about_data")
                ],
                [
                    InlineKeyboardButton("🖥️ 𝙷𝚘𝚠 𝚝𝚘 𝙳𝚎𝚙𝚕𝚘𝚢 🖥️", url="https://youtu.be/KrpqqNNLUSU")
                ]
            ]
        ),
        reply_to_message_id=message.message_id
    )


@trojanz.on_message(filters.command('about') & filters.private)
async def about(client, message):
    await message.reply_text(
        text=Script.ABOUT_MSG,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "⛓️ 𝚂𝙾𝚄𝚁𝙲𝙴 𝙲𝙾𝙳𝙴 ⛓️", url="https://github.com/MRK-YT/Unlimited-Filter-Bot")
                ],
                [
                    InlineKeyboardButton("🔙 𝙱𝚊𝚌𝚔", callback_data="help_data"),
                    InlineKeyboardButton("𝙲𝚕𝚘𝚜𝚎 🔐", callback_data="close_data"),
                ]                
            ]
        ),
        reply_to_message_id=message.message_id
    )
