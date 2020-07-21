import requests
from bs4 import BeautifulSoup


class Chapter:
    __slots__ = (
        "id", "session", "timestamp", "hash", "volume", "chapter", "title", "lang_name",
        "lang_code", "manga_id", "page_array"
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

    def download_chapter(self, path = ""):
        count = 0

        for page in self.page_array:
            img_resp = requests.get(
                f"https://mangadex.org/data/{self.hash}/{page}").content

            with open(f"{path}/chapter_{count}.png", "wb") as img:
                img.write(img_resp)

            count += 1

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
