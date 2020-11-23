import requests
import asyncio
import os
from aiohttp import ClientSession
from bs4 import BeautifulSoup


class Chapter:
    __slots__ = (
        "id", "session", "timestamp", "hash", "volume", "chapter", "title",
        "languageCode", "mangaId", "uploader", "views", "status", "comments", "groups", "mangaTitle", "page_array", "count", "server"
    )

    def __init__(self, session, data):
        self.session = session

        self.id = data["id"]
        self.hash = data["data"]["hash"]
        self.mangaId = data["data"]["mangaId"]
        self.mangaTitle = data["data"]["mangaTitle"]
        self.volume = data["data"]["volume"]
        self.chapter = data["data"]["chapter"]
        self.title = data["data"]["title"]
        self.languageCode = data["data"]["language"]
        self.groups = data["data"]["groups"]
        self.uploader = data["data"]["uploader"]
        self.timestamp = data["data"]["timestamp"]
        self.comments = data["data"]["comments"]
        self.views = data["data"]["views"]
        self.status = data["data"]["status"]
        self.page_array = data["data"]["pages"]
        self.server = data["data"]["server"]
        
        self.count = 0

    def download_chapter(self):
        count = 0

        for page in self.page_array:
            img_resp = requests.get(
                f"https://mangadex.org/data/{self.hash}/{page}").content

            with open(f"{os.getcwd()}/chapter_{count}.png", "wb") as img:
                img.write(img_resp)

            count += 1

    async def __download_file(self, page):
        url = f"https://mangadex.org/data/{self.hash}/{page}"

        async with ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()

                self.count += 1
                with open(f"{os.getcwd()}/chapter_{self.count}.png", "wb") as img:
                    img.write(content)

    async def async_download_chapter(self):
        await asyncio.gather(
            *[self.__download_file(page) for page in self.page_array]
        )

    def get_comments(self):
        json_to_return = {}
        response = self.session.get(
            f"https://mangadex.org/chapter/{self.id}/comments")
        soup = BeautifulSoup(response.content, "html.parser")

        for comment in soup.find_all("tr", "post"):  # comments
            username = comment.td.div.a.text

            json_to_return[f"{username}"] = {
                "user_id": comment.td.div.a["href"],
                "user_avatar": comment.td.img["src"],
                "comment_age": comment.contents[3].contents[2].text,
                "comment": comment.contents[3].contents[5].text
            }
        return json_to_return
