import requests
import asyncio
import os
import json
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from .manga import Manga
from .chapter import Chapter
from .user import User
from .group import Group


class Mangadex():
    def __init__(self):
        self.url = "https://mangadex.org"
        self.session = requests.Session()
        self.session.headers = {
            "authority": "mangadex.org",
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7',
            "pragma": "no-cache",
            'referer': 'https://mangadex.org/',
        }
        self.__session = None
        self.user = None

    def __initializeClientuser(self):
        resp = self.session.get("https://mangadex.org/api/v2/user/me", params= {"include": "chapters"})
        if not resp.status_code == 200:
            if resp.status_code == 404:
                raise Exception(resp)
            raise Exception(f"Can't connect to website. Status code: {resp.status_code}")
        resp = resp.json()
        self.user = User(resp["data"]["user"]["id"], self.session, resp["data"])
        self.user.settings = self.__clientSettingsfunction
        self.user.followed_mangas = self.__clientFollowedmanga
        self.user.ratings = self.__clientUserratings
        self.user.mangaData = self.__clientMangaData
        
    def __clientSettingsfunction(self):
        resp = self.session.get(f"https://mangadex.org/api/v2/user/me/settings")
        if not resp.status_code == 200:
            if resp.status_code == 400:
                raise Exception("No valid ID provided. make sure that you logged in.")
            raise Exception(f"Can't get settings. Status code: {resp.status_code}")
        return resp.json()["data"]

    def __clientFollowedmanga(self):
        resp = self.session.get(f"https://mangadex.org/api/v2/user/me/followed-manga")
        if not resp.status_code == 200:
            if resp.status_code == 400:
                raise Exception("No valid ID provided. make sure that you logged in.")
            raise Exception(f"Can't get followed manga(s). Status code: {resp.status_code}")
        return resp.json()["data"]

    def __clientUserratings(self):
        resp = self.session.get(f"https://mangadex.org/api/v2/user/me/ratings")
        if not resp.status_code == 200:
            if resp.status_code == 400:
                raise Exception("No valid ID provided. make sure that you logged in.")
            raise Exception(f"Can't get ratings. Status code: {resp.status_code}")
        return resp.json()["data"]

    def __clientMangaData(self, manga_id: int) -> dict:
        """
            Get a user's personal data for any given manga.
        """
        resp = self.session.get(f"https://mangadex.org/api/v2/user/me/manga/{manga_id}")
        if not resp.status_code == 200:
            if resp.status_code == 400:
                raise Exception("No valid ID provided. make sure that you logged in.")
            raise Exception(f"Can't get manga data. Status code: {resp.status_code}")
        return resp.json()["data"]

    def __writeSession(self):
        if not self.__session is None:
            with open("./pytmangadex/session.txt", "w", encoding="utf-8") as file:
                file.write(str(self.__session).replace("\'", "\""))

    def login(self, username: str, password: str) -> None:
        login_url = f"{self.url}/ajax/actions.ajax.php?function=login"

        login_data = {
            "login_username": username,
            "login_password": password
        }

        headers = {
            "method": "POST",
            "path": "/ajax/actions.ajax.php?function=login",
            "scheme": "https",
            "Accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "content-length": "367",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://mangadex.org",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
        }

        if os.path.exists("./pytmangadex/session.txt"):
            with open("./pytmangadex/session.txt", "r") as file:
                self.session.cookies.update(json.loads(file.read()))
                self.loginCookies = self.session.cookies
            
            self.__initializeClientuser()
            resp = self.session.get("https://mangadex.org/follows")
            if resp.status_code == 200:
                return

        try:
            is_success = self.session.post(login_url, data=login_data, headers=headers)
            if not is_success.cookies.get("mangadex_session"):
                raise Exception("Failed to login")
            self.loginCookies = self.session.cookies.get_dict()
            self.__session = self.session.cookies.get_dict()
            self.__writeSession()
            self.__initializeClientuser()
        except Exception as err:
            return err

    async def getManga(self, manga_id: int) -> Manga:
        params = {
            "include": "chapters"
        }
        async with ClientSession() as session:
            async with session.get(f"https://mangadex.org/api/v2/manga/{manga_id}", params=params, cookies=self.loginCookies) as mangaResp:
                if not mangaResp.status == 200:
                    raise Exception(f"Can't get manga info. Status Code: {mangaResp.status}")
                
                mangaResp = json.loads(
                    await mangaResp.text()
                )
                
                if mangaResp:
                    return Manga(manga_id, self.session, mangaResp)

    def get_manga(self, manga_id: int) -> Manga:
        params = {
            "include": "chapters"
        }
        mangaResp = requests.get(f"https://mangadex.org/api/v2/manga/{manga_id}", params=params)
        if not mangaResp.status_code == 200:
            raise Exception(f"Can't get manga info. Status Code: {mangaResp.status_code}")
        mangaResp = mangaResp.json()

        if mangaResp:
            return Manga(manga_id, self.session, mangaResp)

    def get_chapter(self, chapter_id: int) -> Chapter:
        data = self.session.get(
            f"https://mangadex.org/api/v2/chapter/{chapter_id}").json()

        if data:
            return Chapter(self.session, data["data"])

    def get_user(self, user_id: int=None, me=False) -> User:
        if not me:
            if user_id is None:
                raise Exception("user_id is a required argument")
            else:
                try:
                    int(user_id)
                except:
                    raise Exception("user_id must be int!")
            requestUrl = f"{self.url}/api/v2/user/{user_id}"
        else:
            requestUrl = f"{self.url}/api/v2/user/me"

        resp = self.session.get(requestUrl, params= {"include": "chapters"})
        if not resp.status_code == 200:
            if resp.status_code == 404:
                raise Exception(resp)
            raise Exception(f"Can't connect to website. Status code: {resp.status_code}")
        resp = resp.json()

        return User(resp["data"]["user"]["id"], self.session, resp["data"])

    def get_group(self, group_id: int) -> Group:
        params = {
            "include": "chapters"
        }
        resp = self.session.get(f"https://mangadex.org/api/v2/group/{group_id}", params=params)
        if not resp.status_code == 200:
            if resp.status_code == 404:
                raise Exception(resp)
            raise Exception(f"Can't connect to website. Status code: {resp.status_code}")
        resp = resp.json()

        return Group(self.session, resp["data"])

    def follow_last_updateds(self, limit=30) -> Chapter: # This will be deprecated. Instead use same function from user
        print("This method will be deprecated. Instead use same function from user class")

        resp = self.session.get(f"{self.url}/api/v2/user/me/followed-updates")
        if not resp.status_code == 200:
            if resp.status_code == 404:
                raise Exception(resp)
            raise Exception(f"Can't connect to website. Status code: {resp.status_code}")
        resp = resp.json()

        return [
            Chapter(self.session, chapter) for chapter in resp["data"]["chapters"][:limit]
        ]

    def last_updates(self) -> dict:
        json_to_return = {}
        count = 0
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        contents = soup.find(class_="row m-0")

        for manga_div in contents:
            json_to_return[f"{count}"] = {
                "chapter_link": manga_div.div.a["href"],
                "chapter_thumbnail": manga_div.div.img["src"],
                "chapter": manga_div.contents[5].a.string,
                "title": manga_div.contents[3].a["title"],
                "group_link": manga_div.contents[7].a["href"],
                "group": manga_div.contents[7].a.string,
                "age": manga_div.contents[9].text
            }
            count += 1

        return json_to_return

    def top_manga(self) -> dict:
        json_to_return = {}
        count = 0
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        top_mangas = soup.find(id="top_follows")
        top_manga_content = top_mangas.ul

        for manga in top_manga_content:
            json_to_return[f"{count}"] = {
                "thumbnail_link": manga.a["href"],
                "thumbnail": manga.a.img["src"],
                "title": manga.contents[3].a.string,
                "manga_link": manga.contents[3].a["href"],
                "follow_count": manga.contents[5].span.text,
                "star_rating": manga.contents[5].contents[2].span.text,
                "users": manga.contents[5].small.text
            }
            count += 1

        return json_to_return

    def latest_posts_forums(self) -> dict:
        json_to_return = {}
        count = 0
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        for forum in soup.find(id="forum_posts").ul:
            json_to_return[f"{count}"] = {
                "thread_link": forum.div.a["href"],
                "forum_title": forum.p.a.text,
                "forum_post_link": forum.p.a["href"],
                "forum_comment": forum.contents[5].text.replace("\r\n", "")
            }
            count += 1
        return json_to_return

    def latest_posts_manga(self) -> dict:
        json_to_return = {}
        count = 0
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        for forum in soup.find(id="manga_posts").ul:
            try:
                json_to_return[f"{count}"] = {
                    "thread_link": forum.div.a["href"],
                    "thread_thumbnail": forum.div.img["src"],
                    "manga_title": forum.p.a.text,
                    "manga_post_link": forum.p.a["href"],
                    "manga_comment": forum.contents[5].text.replace("\r\n", "")
                }
            except:
                return "no comment to display"
            count += 1
        return json_to_return

    def featured_titles(self) -> dict:
        json_to_return = {}
        count = 0
        response = self.session.get(f"{self.url}/featured")
        soup = BeautifulSoup(response.content, "html.parser")

        for title in soup.find_all("div", "manga-entry col-lg-6 border-bottom pl-0 my-1"):
            json_to_return[f"{count}"] = {
                "manga_link": title.div.a["href"],
                "manga_img": title.div.img["src"],
                "manga_title": title.contents[3].a.text,
                "bayesian_rating": title.ul.li.contents[4].text,
                "follows": title.ul.contents[3].text,
                "views": title.ul.contents[5].text,
                "comment_link": title.ul.contents[7].a["href"],
                "comment_count": title.ul.contents[7].a.text,
                "description": title.contents[7].text
            }

            count += 1

        return json_to_return

    async def search(self, keywords: str, limit: int = 10) -> Manga:
        params = {
            "title": keywords
        }
        resp = self.session.get(f"{self.url}/search", params=params)
        if not resp.status_code == 200:
            raise Exception(f"Cant get results {resp.status_code}")

        soup = BeautifulSoup(resp.content, "html.parser")
        titles = soup.find_all(class_="ml-1 manga_title text-truncate")
        manga_ids = [manga_id["href"].split("/")[2] for manga_id in titles]

        for mangaId in manga_ids[:limit]:
            yield await self.getManga(mangaId)

    def runNotifications(self):
        loop = asyncio.get_event_loop()
        loop.run_forever()
