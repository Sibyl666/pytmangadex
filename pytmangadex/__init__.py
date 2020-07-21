import requests
from bs4 import BeautifulSoup
from .manga import Manga
from .chapter import Chapter


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

    def login(self, username, password):
        login_url = f"{self.url}ajax/actions.ajax.php?function=login"

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

        try:
            is_success = self.session.post(login_url, data=login_data, headers=headers)
            if not is_success.cookies.get("mangadex_session"):
                return "Failed To Login"
            print("logged in")

        except Exception as err:
            return err

    def get_manga(self, manga_id: int):
        data = self.session.get(f"https://mangadex.org/api/?id={manga_id}&type=manga").json()

        resp_web = self.session.get(f"https://mangadex.org/title/{manga_id}")
        soup = BeautifulSoup(resp_web.content, "lxml")
        for prop in soup.find_all(class_="row m-0 py-1 px-0 border-top"):
            prop_name = prop.contents[1].text.strip().replace(":", "")
            value = prop.contents[3].text.strip()

            if prop_name == "Genre":
                value = []
                for genre in prop.contents[3]:
                    try:
                        value.append(genre.text)
                    except:
                        continue
                data["manga"]["genres"] = value

            if prop_name == "Theme":
                # themes
                value = []
                for theme in prop.contents[3]:
                    try:
                        value.append(theme.text)
                    except:
                        continue
                data["manga"][f"{prop_name}"] = value

            if prop_name == "Stats":
                stat = prop.contents[3].ul.contents
                value = {
                    "views": stat[1].text,
                    "follows": stat[3].text,
                    "total_chapters": stat[5].text
                }
                data["manga"][f"{prop_name}"] = value

        if data:
            return Manga(manga_id, self.session, data)

    def get_chapter(self, chapter_id: int):
        data = self.session.get(
            f"https://mangadex.org/api/?id={chapter_id}&server=null&saver=0&type=chapter").json()

        if data:
            return Chapter(self.session, data)

    def follow_last_updateds(self):
        json_to_return = {}
        count = 0
        follow_url = f"{self.url}/follows"
        response = self.session.get(follow_url)

        soup = BeautifulSoup(response.content, "lxml")
        contents = soup.find_all(class_="row no-gutters")

        # GET TITLE
        for manga_div in contents[1:]:
            contents_in_div = manga_div.contents
            try:
                json_to_return[f"{count}"] = {
                    "title": contents_in_div[1].a['title'],
                    "chapter": contents_in_div[5].div.contents[3].a.string,
                    "translator": contents_in_div[5].div.contents[13].a.string,
                    "uploader": contents_in_div[5].div.contents[15].a.string,
                    "age": contents_in_div[5].div.contents[7].text.strip(),
                    "comments_href": contents_in_div[5].div.contents[5].a['href'],
                    "comments_count": contents_in_div[5].div.contents[5].a.span['title']
                }
                count += 1
            except:
                pass

        return json_to_return

    def last_updates(self):
        json_to_return = {}
        count = 0
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, "lxml")
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

    def top_manga(self):
        json_to_return = {}
        count = 0
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, "lxml")
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

    def latest_posts_forums(self):
        json_to_return = {}
        count = 0
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, "lxml")

        for forum in soup.find(id="forum_posts").ul:
            json_to_return[f"{count}"] = {
                "thread_link": forum.div.a["href"],
                "forum_title": forum.p.a.text,
                "forum_post_link": forum.p.a["href"],
                "forum_comment": forum.contents[5].text.replace("\r\n", "")
            }
            count += 1
        return json_to_return

    def latest_posts_manga(self):
        json_to_return = {}
        count = 0
        response = self.session.get(self.url)
        soup = BeautifulSoup(response.content, "lxml")

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

    def featured_titles(self):
        json_to_return = {}
        count = 0
        response = self.session.get(f"{self.url}/featured")
        soup = BeautifulSoup(response.content, "lxml")

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
