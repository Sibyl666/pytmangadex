from .chapter import Chapter
from .manga import Manga
import requests

class User:
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

        self.chapters = [Chapter(self.session, chapter) for chapter in data["chapters"] if chapter["id"]]

    # def get_my_settings(self) -> dict:
    #     """
    #         Get a user's website settings.
    #     """
    #     resp = self.session.get(f"https://mangadex.org/api/v2/user/{self.user_id}/settings")
    #     if not resp.status_code == 200:
    #         if resp.status_code == 400:
    #             raise Exception("No valid ID provided. make sure that you logged in.")
    #         raise Exception(f"Can't get settings. Status code: {resp.status_code}")
    #     return resp.json()["data"]

    # def get_user_followed_manga(self) -> Manga:
    #     """
    #         Get a user's followed manga and personal data for them.
    #     """
    #     resp = self.session.get(f"https://mangadex.org/api/v2/user/{self.user_id}/followed-manga")
    #     if not resp.status_code == 200:
    #         if resp.status_code == 400:
    #             raise Exception("No valid ID provided. make sure that you logged in.")
    #         raise Exception(f"Can't get settings. Status code: {resp.status_code}")
    #     return resp.json()["data"]

    # def get_user_followed_chapter_updates(self) -> dict:
    #     """
    #         Get the latest uploaded chapters for the manga that the user has followed, as well as basic related manga information.
    #         Ordered by timestamp descending (the datetime when the chapter is available).
    #         Limit 100 chapters per page.
    #         Note that the results are automatically filtered by the authorized user's chapter language filter setting.
    #     """
    #     resp = self.session.get(f"https://mangadex.org/api/v2/user/{self.user_id}/followed-updates")
    #     if not resp.status_code == 200:
    #         if resp.status_code == 400:
    #             raise Exception("No valid ID provided. make sure that you logged in.")
    #         raise Exception(f"Can't get settings. Status code: {resp.status_code}")
    #     return resp.json()["data"]

    # def get_user_ratings(self) -> dict:
    #     """
    #         Get a user's manga ratings.
    #     """
    #     resp = self.session.get(f"https://mangadex.org/api/v2/user/{self.user_id}/ratings")
    #     if not resp.status_code == 200:
    #         if resp.status_code == 400:
    #             raise Exception("No valid ID provided. make sure that you logged in.")
    #         raise Exception(f"Can't get settings. Status code: {resp.status_code}")
    #     return resp.json()["data"]

    # def get_user_manga_data(self, manga_id: int) -> dict:
    #     """
    #         Get a user's personal data for any given manga.
    #     """
    #     resp = self.session.get(f"https://mangadex.org/api/v2/user/{self.user_id}/manga")
    #     if not resp.status_code == 200:
    #         if resp.status_code == 400:
    #             raise Exception("No valid ID provided. make sure that you logged in.")
    #         raise Exception(f"Can't get settings. Status code: {resp.status_code}")
    #     return resp.json()["data"]
