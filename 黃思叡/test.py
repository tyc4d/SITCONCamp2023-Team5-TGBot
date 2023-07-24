from bs4 import BeautifulSoup
import requests

import webbrowser
from youtubesearchpython import VideosSearch


def findYT(search_words):
    id = VideosSearch(search_words, limit=2).result()["result"][0]["id"]
    # print(reuslt)
    youtube_url = f"https://www.youtube.com/watch?v={id}"
    return youtube_url


search_word = "abc"

print("success")
print(findYT(search_word))