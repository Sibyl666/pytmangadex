import asyncio
import json
import os
import re
import requests
from ..chapter import Chapter
from datetime import datetime, timedelta
from pytmangadex import Mangadex
from bs4 import BeautifulSoup
from aiohttp import ClientSession


class Notification:
    def __init__(self, function):
        self.function = function
        # self.sleep_until = sleep_until
        self.loop = asyncio.get_event_loop()
        self.url = "https://mangadex.org"
        self.session = requests.Session()

        self.headers = {
            "authority": "mangadex.org",
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7',
            "pragma": "no-cache",
            'referer': 'https://mangadex.org/',
        }
        self.sentchapters()

    def sentchapters(self):
        if os.path.exists("./pytmangadex/sent.json"):
            with open("./pytmangadex/sent.json", "r") as file:
                self.__sentchapters = json.loads(file.read())
        else:
            self.__sentchapters = {
                "sent": []
            }

    def write_sent(self, chapter_id):
        self.__sentchapters["sent"].append(chapter_id)
        with open("./pytmangadex/sent.json", "w") as file:
            file.write(
                json.dumps(
                    self.__sentchapters, indent=4
                )
            )

    def getCookies(self):
        with open("./pytmangadex/session.txt", "r", encoding="utf-8") as file:
            return json.loads(file.read().replace("'", "\""))

    async def makeRequest(self):
        async with ClientSession() as session:
            async with session.get(f"{self.url}/api/v2/user/me/followed-updates", cookies=self.getCookies(), headers=self.headers) as resp:
                if not resp.status == 200:
                    raise Exception(f"Cant connect to website {resp.status}")
                content = json.loads(await resp.read())

        now = datetime.now()
        for chapter in content["data"]["chapters"]:
            if chapter["id"] in self.__sentchapters["sent"]:
                continue

            chapterDate = datetime.fromtimestamp(chapter["timestamp"])
            ago = now - chapterDate
            if ago < timedelta(minutes=2):
                self.write_sent(chapter["id"])
                return Chapter(self.session.cookies.update(self.getCookies()), chapter)

        return False

    async def __loop(self, *args, **kwargs):
        while True:
            chapter = await self.makeRequest()
            if chapter:
                await self.function(chapter)
            await asyncio.sleep(30)

    def add(self):
        self._task = self.loop.create_task(self.__loop())
        return self._task


def ChapterNotification(function):
    return Notification(function)
