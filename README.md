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
```python
class Mangadex():
    def __init__(self):

    #Login first
    def login(self, username, password):
    
    #Async version of get_manga
    async def getManga(self, manda_id: int):

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

    #Search manga
    async def search(self, keywords: str, limit: int = 10):

    #For running ChapterNotification functions
    def runNotifications(self):

```

# Manga class
```python
class Manga:

    #Manga attributes like manga.title etc.
    def __init__(self, manga_id, session, data):

    #Returns covers manga had
    def covers(self):

    #Get chapter tags with info description etc.
    def getTags(self):
```

# Chapter class
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

# Examples
## Base
```python
from pytmangadex import Mangadex

client = Mangadex()
client.login("username", "password")

async def main():
    # other examples down there will come here

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