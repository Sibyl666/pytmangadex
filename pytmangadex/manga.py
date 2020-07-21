import requests
from .chapter import Chapter


class Manga:
    __slots__ = (
        "session", "manga_id", "cover_url", "description", "title", "alt_names", "artist", "author", "status", "genres",
        "last_chapter", "lang_name", "lang_flag", "hentai", "links", "rating", "groups","chapters"
    )

    def __init__(self, manga_id, session, data):
        self.session = session
        self.manga_id = manga_id

        self.cover_url = data["manga"]["cover_url"]
        self.description = data["manga"]["description"]
        self.title = data["manga"]["title"]
        self.alt_names = data["manga"]["alt_names"]
        self.artist = data["manga"]["artist"]
        self.author = data["manga"]["author"]
        self.status = data["manga"]["status"]
        self.genres = data["manga"]["genres"]
        self.last_chapter = data["manga"]["last_chapter"]
        self.lang_name = data["manga"]["lang_name"]
        self.lang_flag = data["manga"]["lang_flag"]
        self.hentai = data["manga"]["hentai"]
        self.links = data["manga"]["links"]
        self.rating = data["manga"]["rating"]

        self.groups = data["group"]
        self.chapters = data["chapter"]

    def covers(self):
        resp = self.session.get(f"https://mangadex.org/api/?id={self.manga_id}&type=covers").json()

        if resp:
            return resp
