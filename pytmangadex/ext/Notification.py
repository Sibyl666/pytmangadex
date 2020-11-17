import asyncio
import json
import os
import re
from pytmangadex import Mangadex
from bs4 import BeautifulSoup
from aiohttp import ClientSession


class Notification:
    def __init__(self, function):
        self.function = function
        # self.sleep_until = sleep_until
        self.loop = asyncio.get_event_loop()
        self.url = "https://mangadex.org"

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
            async with session.get(f"{self.url}/follows", cookies=self.getCookies(), headers=self.headers) as resp:

                if not resp.status == 200:
                    raise Exception(f"Cant connect to website {resp.status}")
                content = await resp.read()

        soup = BeautifulSoup(content.decode(), "lxml")
        contents = soup.find_all(class_="row no-gutters")

        # GET TITLE
        count = 0
        json_to_return = {}
        for manga_div in contents[0:]:
            contents_in_div = manga_div.contents
            try:
                json_to_return[f"{count}"] = {
                    "title": contents_in_div[1].a['title'],
                    "chapterId": contents_in_div[1].a['href'].split("/")[2],
                    "chapter": contents_in_div[5].div.contents[3].a.string,
                    "translator": contents_in_div[5].div.contents[13].a.string,
                    "uploader": contents_in_div[5].div.contents[15].a.string,
                    "age": contents_in_div[5].div.contents[7].text.strip(),
                }

                try:
                    json_to_return[str(count)]["comments_href"] = contents_in_div[5].div.contents[5].a['href'],
                    json_to_return[str(count)]["comments_count"] = contents_in_div[5].div.contents[5].a.span['title']
                except:
                    json_to_return[str(count)]["comments_href"] = None,
                    json_to_return[str(count)]["comments_count"] = None
                
                count += 1
            except:
                pass

        for manga in json_to_return:
            if json_to_return[manga]["chapterId"] in self.__sentchapters["sent"]:
                continue

            match = re.match("(1|2) (min|mins) ago", json_to_return[manga]["age"])
            if match:
                self.write_sent(json_to_return[manga]["chapterId"])
                return json_to_return[manga]

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
