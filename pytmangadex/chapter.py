import requests
import asyncio
import os
from aiohttp import ClientSession
from bs4 import BeautifulSoup


class Chapter:
    __slots__ = (
        "id", "data", "session", "timestamp", "hash", "volume", "chapter", "title",
        "languageCode", "mangaId", "uploader", "views", "comments", "groups", "mangaTitle", "page_array", "count",
        "__pagesrequestdata", "__pages", "__status", "__server"
    )

    def __init__(self, session, data):
        self.data = data

        self.session = session
        self.id = data["id"]
        self.hash = data["hash"]
        self.mangaId = data["mangaId"]
        self.mangaTitle = data["mangaTitle"]
        self.volume = data["volume"]
        self.chapter = data["chapter"]
        self.title = data["title"]
        self.languageCode = data["language"]
        self.groups = data["groups"]
        self.uploader = data["uploader"]
        self.timestamp = data["timestamp"]
        self.comments = data["comments"]
        self.views = data["views"]
        self.count = 0
        
        self.__pagesrequestdata = None

    @property
    def pages(self):
        if "pages" in self.data.keys():
            return self.data["pages"]

        if self.__pagesrequestdata is not None:
            self.__pages = self.__pagesrequestdata["pages"]
            return self.__pages
        else:
            resp = requests.get(f"https://mangadex.org/api/v2/chapter/{self.id}")
            if resp.status_code == 200:
                resp = resp.json()
                self.__pagesrequestdata = resp["data"]
                self.__pages = resp["data"]["pages"]
                return self.__pages

    @property
    def status(self):
        if "status" in self.data.keys():
            return self.data["status"]

        if self.__pagesrequestdata is not None:
            self.__status = self.__pagesrequestdata["status"]
            return self.__status
        else:
            resp = requests.get(f"https://mangadex.org/api/v2/chapter/{self.id}")
            if resp.status_code == 200:
                resp = resp.json()
                self.__pagesrequestdata = resp["data"]
                self.__status = self.__pagesrequestdata["status"]
                return self.__status

    @property
    def server(self):
        if "server" in self.data.keys():
            return self.data["server"]

        if self.__pagesrequestdata is not None:
            self.__server = self.__pagesrequestdata["server"]
            return self.__server
        else:
            resp = requests.get(f"https://mangadex.org/api/v2/chapter/{self.id}")
            if resp.status_code == 200:
                resp = resp.json()
                self.__pagesrequestdata = resp["data"]
                self.__server = self.__pagesrequestdata["server"]
                return self.__server

    def download_chapter(self):
        count = 0

        for page in self.pages:
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
            *[self.__download_file(page) for page in self.pages]
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
