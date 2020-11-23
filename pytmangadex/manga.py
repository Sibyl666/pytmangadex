import requests
from aiohttp import ClientSession
from .chapter import Chapter


class Manga:
    __slots__ = (
        "session", "manga_id", "mainCover", "description", "lastVolume", "title", "altTitles", "artist", "author", "status", "genres",
        "lastChapter", "publication", "relations", "tags", "allTags", "isHentai", "links", "rating", "groups","chapters"
    )

    def __init__(self, manga_id, session, data):
        self.session = session
        self.manga_id = manga_id
        
        self.title = data["data"]["manga"]["title"]
        self.altTitles = data["data"]["manga"]["altTitles"]
        self.description = data["data"]["manga"]["description"]
        self.artist = data["data"]["manga"]["artist"]
        self.author = data["data"]["manga"]["author"]
        self.publication = data["data"]["manga"]["publication"]

        self.tags = data["data"]["manga"]["tags"]

        self.mainCover = data["data"]["manga"]["mainCover"]
        self.lastVolume = data["data"]["manga"]["lastVolume"]
        self.lastChapter = data["data"]["manga"]["lastChapter"]
        self.isHentai = data["data"]["manga"]["isHentai"]
        self.links = data["data"]["manga"]["links"]
        self.relations = data["data"]["manga"]["relations"]
        self.rating = data["data"]["manga"]["rating"]

        self.groups = data["data"]["groups"]
        self.chapters = data["data"]["chapters"]

    def getTags(self):
        self.allTags = self.session.get("https://mangadex.org/api/v2/tag").json()
        self.tags = [self.allTags["data"][tag] for tag in self.allTags["data"] if int(tag) in self.tags]
        return self.tags

    def covers(self):
        resp = self.session.get(f"https://mangadex.org/api/?id={self.manga_id}&type=covers").json()

        if resp:
            return resp
