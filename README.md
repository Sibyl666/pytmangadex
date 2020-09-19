# Mangadexpy
an library to scrape data from mangadex.org

# basic usage

```python
from pytmangadex import Mangadex

mangadex = Mangadex()
mangadex.login("username", "password")

mang = mangadex.get_manga(33326)
print(mang.title)
>>> That Girl Is Not Just Cute

chapter = mangadex.get_chapter(966015)
print(chapter.get_comments())
>>> Long json thing

print(chapter.download_chapter("manga/")) #download to the manga folder

```
# API Functions
```python
class Mangadex():
    def __init__(self):

    #Login first
    def login(self, username, password):
    
    #Returns you an manga object
    def get_manga(self, manga_id: int):

    #Returns you an chapter object
    def get_chapter(self, chapter_id: int):

    #Returns last updated chapters of following manga's
    def follow_last_updateds(self):

    #Returns all last updates manga's
    def last_updates(self):

    #Returns top manga's list has the most followers
    def top_manga(self):

    def latest_posts_forums(self):

    def latest_posts_manga(self):

    def featured_titles(self):

```

# Manga class
```python
class Manga:

    #Manga attributes like manga.title etc.
    def __init__(self, manga_id, session, data):

    #Returns covers manga had
    def covers(self):
```

# Chapter class
```python
class Chapter:

    #Chapter attributes like chapter.title
    def __init__(self, session, data):

    #Downloads chapter to the given path
    #if empty will download to the cwd
    def download_chapter(self):
    
    def async_download_chapter(self):

    #Returns json of comments on chapter
    def get_comments(self):

```
