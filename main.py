# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
import requests 
from dotenv import load_dotenv
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import *


load_dotenv()
API = "https://api.abirhasan.wtf/google?query="


Bot = Client(
    "Google-Search-Bot",
    bot_token="6032076608:AAG4I-T-zlITKKPwninOyBZeMkhzdBG6Wao",
    api_id="17983098",
    api_hash="ee28199396e0925f1f44d945ac174f64"
)


START_TEXT = """Hello {}
I am a google search bot. \
Send a text for google search result.

> `I can search from google. Use me in inline.`

Made by @FayasNoushad"""

JOIN_BUTTON = [
    InlineKeyboardButton(
        text='⚙ Join Updates Channel ⚙',
        url='https://telegram.me/FayasNoushad'
    )
]


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        reply_markup=InlineKeyboardMarkup([JOIN_BUTTON]),
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.text)
async def filter(bot, update):
    await update.reply_text(
        text="`Click the button below for searching...`",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Search Here", switch_inline_query_current_chat=update.text)],
                [InlineKeyboardButton(text="Search in another chat", switch_inline_query=update.text)]
            ]
        ),
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_inline_query()
async def inline(bot, update):
    results = google(update.query)
    answers = []
    for result in results:
        answers.append(
            InlineQueryResultArticle(
                title=result["title"],
                description=result["description"],
                input_message_content=InputTextMessageContent(
                    message_text=result["text"],
                    disable_web_page_preview=True
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="Link", url=result["link"])],
                        JOIN_BUTTON
                    ]
                )
            )
        )
    await update.answer(answers)


def google(query):
    r = requests.get(API + requote_uri(query))
    informations = r.json()["results"][:50]
    results = []
    for info in informations:
        text = f"**Title:** `{info['title']}`"
        text += f"\n**Description:** `{info['description']}`"
        text += f"\n\nMade by @FayasNoushad"
        results.append(
            {
                "title": info['title'],
                "description": info['description'],
                "text": text,
                "link": info['link']
            }
        )
    return results


Bot.run()
