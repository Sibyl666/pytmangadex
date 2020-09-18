import requests
import asyncio
import os
from aiohttp import ClientSession
from bs4 import BeautifulSoup


class Chapter:
    __slots__ = (
        "id", "session", "timestamp", "hash", "volume", "chapter", "title", "lang_name",
        "lang_code", "manga_id", "page_array", "count"
    )

    def __init__(self, session, data):
        self.session = session

        self.id = data["id"]
        self.timestamp = data["timestamp"]
        self.hash = data["hash"]
        self.volume = data["volume"]
        self.chapter = data["chapter"]
        self.title = data["title"]
        self.lang_name = data["lang_name"]
        self.lang_code = data["lang_code"]
        self.manga_id = data["manga_id"]
        self.page_array = data["page_array"]
        self.count = 0

    def download_chapter(self):
        count = 0

        for page in self.page_array:
            img_resp = requests.get(
                f"https://mangadex.org/data/{self.hash}/{page}").content

            with open(f"{os.getcwd()}/chapter_{count}.png", "wb") as img:
                img.write(img_resp)

            count += 1

    async def download_file(self, page):
        url = f"https://mangadex.org/data/{self.hash}/{page}"

        async with ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()

                self.count += 1
                with open(f"{os.getcwd()}/chapter_{self.count}.png", "wb") as img:
                    img.write(content)

    async def async_download_chapter(self):
        await asyncio.gather(
            *[self.download_file(page) for page in self.page_array]
        )

    def get_comments(self):
        json_to_return = {}
        response = self.session.get(
            f"https://mangadex.org/chapter/{self.id}/comments")
        soup = BeautifulSoup(response.content, "lxml")

        for comment in soup.find_all("tr", "post"):  # comments
            username = comment.td.div.a.text

            json_to_return[f"{username}"] = {
                "user_id": comment.td.div.a["href"],
                "user_avatar": comment.td.img["src"],
                "comment_age": comment.contents[3].contents[2].text,
                "comment": comment.contents[3].contents[5].text
            }
        return json_to_return
