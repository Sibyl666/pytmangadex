from .chapter import Chapter
from .manga import Manga
import requests

class User:
    __slots__ = (
        "user_id", "session", "data", "username", "levelId", "joined", "lastSeen", "website",
        "biography", "views", "uploads", "premium", "mdAtHome", "avatar", "chapters", "settings",
        "followed_mangas", "ratings", "mangaData"
    )

    def __init__(self, user_id, session, data):
        self.user_id = user_id
        self.session = session
        self.data = data
        
        self.username = data["user"]["username"]
        self.levelId = data["user"]["levelId"]
        self.joined = data["user"]["joined"]
        self.lastSeen = data["user"]["lastSeen"]
        self.website = data["user"]["website"]
        self.biography = data["user"]["biography"]
        self.views = data["user"]["views"]
        self.uploads = data["user"]["uploads"]
        self.premium = data["user"]["premium"]
        self.mdAtHome = data["user"]["mdAtHome"]
        self.avatar = data["user"]["avatar"]

        self.settings = None
        self.followed_mangas = None
        self.ratings = None
        self.mangaData = None

        self.chapters = [Chapter(self.session, chapter) for chapter in data["chapters"] if chapter["id"]]
