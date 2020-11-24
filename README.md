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

chapter.download_chapter("manga/") #download to the manga folder

```

# Auto Notification
```python
from pytmangadex import Mangadex
from pytmangadex.ext.Notification import ChapterNotification

client = Mangadex()

@ChapterNotification
async def followNotification(chapter): # param chapter is Chapter object
    print(chapter["title"])

client.login("username", "password")
followNotification.add()
client.runNotifications() # This should be last thing in the code 
                          # If you use library like discord py only .add() function is enough so you don't need this
```


# API Functions
### Attribute List, (same with user object but has extra methods)
user is the user object of account that logged in. \
user.settings \
user.followed_mangas \
user.ratings
```python
user
```
```python
class Mangadex():
    def __init__(self):

    #Login first
    def login(self, username: str, password: str) -> None:
    
    #Async version of get_manga
    async def getManga(self, manda_id: int) -> Manga:

    #Returns you an manga object
    def get_manga(self, manga_id: int) -> Manga:

    #Returns you an chapter object
    def get_chapter(self, chapter_id: int) -> Chapter:

    #Returns user object
    def get_user(self, user_id: int=None, me=False) -> User:

    #Returns last updated chapters of following manga's
    def follow_last_updateds(self) -> Chapter:

    #Returns all last updates manga's
    def last_updates(self) -> dict:

    #Returns top manga's list has the most followers
    def top_manga(self) -> dict:

    def latest_posts_forums(self) -> dict:

    def latest_posts_manga(self) -> dict:

    def featured_titles(self) -> dict:

    #Search manga
    async def search(self, keywords: str, limit: int = 10) -> Manga:

    #For running ChapterNotification functions
    def runNotifications(self):

```

# Manga class
### Attribute List
```python
manga_id, title, altTitles, description, artist, author, publication, tags, mainCover, lastVolume, lastChapter, isHentai, links, relations, rating, groups, chapters
```
```python
class Manga:
    #Manga attributes like manga.title etc.
    def __init__(self, manga_id, session, data):

    #Returns covers manga had
    def covers(self) -> dict:

    #Get chapter tags with info description etc.
    def getTags(self) -> dict:
```

# Chapter class
### Attribute List
```python
id, hash, mangaId, mangaTitle, volume, chapter, title, languageCode, groups,uploader, timestamp, comments, views, pages, status, server
```
```python
class Chapter:

    #Chapter attributes like chapter.title
    def __init__(self, session, data):

    #Downloads chapter to the given path
    #if empty will download to the cwd
    def download_chapter(self):
    
    #Async version of downloading chapter
    def async_download_chapter(self):

    #Returns json of comments on chapter
    def get_comments(self):

```
# User class
### Attribute List
```python
username, levelId, joined, lastSeen, website, biography, views, uploads, premium, mdAtHome, avatar, chapters
```
```python
class User:
    #User attributes like user.username etc.
    def __init__(user_id, session, data):
```
# Examples
## Base
```python
from pytmangadex import Mangadex

client = Mangadex()
client.login("username", "password")

async def main():
    # other examples down there will come if its async function like in the search examples

if __name__ == "__main__":
    asyncio.run(main())
```
## How to Search
```python
async for manga in client.search("isekai", 10): # params: Search word, limit
    print(manga.title) # Manga object
```
## Get tags of manga with info
```python
async for manga in client.search("isekai", 10): # params: Search word, limit
    manga.getTags()
    print(manga.title) # Manga object
```
## Get any user
```python
user = mangadex.get_user(20834) # Returns user object
print(user.username)
```