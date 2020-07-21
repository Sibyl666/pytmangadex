# mangadexpy
an library to scrape data from mangadex.org

basic usage
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
