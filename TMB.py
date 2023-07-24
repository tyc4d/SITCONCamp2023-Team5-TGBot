import requests
import urllib.parse
import re
from bs4 import BeautifulSoup
from youtubesearchpython import VideosSearch
from pytube import YouTube
import random,string,os

URL_ROOT = 'http://mojim.com/'

def findYT(search_words):
    id = VideosSearch(search_words, limit=2).result()["result"][0]["id"]
    # print(reuslt)
    youtube_url = f"https://www.youtube.com/watch?v={id}"
    return youtube_url

def search_song(song_name):
    
    song_name += '.html?t3'
    url = urllib.parse.urljoin(URL_ROOT, song_name)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    songs = soup.find_all('dd', re.compile('^mxsh_dd'))
    del songs[0]
    song_list = list()
    for song  in songs:
        meta = song.find('span', 'mxsh_ss4').find('a')
        name_temp = meta.getText().split('.')
        song_list.append({
            'name':name_temp[1],
            'singer':song.find('span', 'mxsh_ss2').getText(),
            'album':song.find('span', 'mxsh_ss3').getText(),
            'link':meta.get('href'),
            })
    return song_list

def get_lyric(url):
    url = urllib.parse.urljoin(URL_ROOT, url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    lyric = soup.find('dl', 'fsZx1')

    a = re.compile('^\[\d+')

    lyric_list = list()
    for string in lyric.stripped_strings:
        if string == '更多更詳盡歌詞 在' or string == '※ Mojim.com 魔鏡歌詞網':
            continue
        if a.match(string):
            break
        lyric_list.append(string)

    singer = lyric_list.pop(0)
    name = lyric_list.pop(0)

    song_detail = {
        'singer':singer,
        'name':name,
        'lyric':lyric_list,
    }
    return song_detail

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
import json
# 請自行填入 API Token
bot = telebot.TeleBot('填入你的Bot API Tokem')

@bot.message_handler(commands=['help', 'start'])
def send_wel(message):
    bot.reply_to(message, """\
/lyrics：用 /lyrics [歌名] 來搜尋特定歌名的完整歌詞
/name：用 /name [歌詞] 來搜尋片段歌詞的可能前10項歌名，其中歌詞中間要用＋間隔
/youtube：用 /youtube [關鍵字] 來搜尋youtube上該關鍵字的第一項搜尋結果
/mp3：用 /mp3 [歌名] 可將特定歌名的 youtube 影片下載成 mp3 檔 + 去人聲 mp3 檔 
""")
@bot.message_handler(commands=['youtube'])
def send_pong(message):
    if message.chat.type in ("supergroup","private"):
        global search_words
        print(message.text)
        search_words =message.text[8:]
        bot.reply_to(message, findYT(search_words))       
                 
@bot.message_handler(commands=['lyrics'])
def send_ly(message):
    if message.chat.type in ("supergroup","private"):
        try:
            search_songName =message.text[7:]
            music_url = search_song(search_songName)[0]['link']
            lyrics = ""
            for lyric in get_lyric(music_url)['lyric']:
                lyrics += lyric
                lyrics += " "
            print(get_lyric(music_url)['lyric'])
            bot.reply_to(message, lyrics) 
        except IndexError:
            bot.reply_to(message, "No result") 

@bot.message_handler(commands=['name'])
def send_ly(message):
    if message.chat.type in ("supergroup","private"):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    a=['+','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ',"'",'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    empty=[]
    n=''
    for i in message.text[5:]:
        bb=False
        for j in a:
            if i==j:
                bb=True
        if bb:
            n+=i.lower()
    n=n.replace(' ','+').replace("'","%27")
    url="https://search.azlyrics.com/search.php?q="+n+"&x=9edbdb599086cfb43be7941b396a8045c2321d488f5a9439d85c879caeb7d340"
    r=requests.get(url,headers=headers)
    soup=BeautifulSoup(r.text, "html.parser")
    s=soup.find_all("a")
    bb=True
    for i in s:
        if bb==False:
            break
        ii=i.find_all("span")
        iii=str(ii)
        if(iii!='[]'):
            k=iii.split('"</b></span>]')
            kk=k[0].split('[<span><b>"')
            if(len(kk)>=2):
                kkk=kk[1]
                if(kkk[-8:]=="</span>]"):
                    kkk=kkk[:-9]
                for j in range(len(kkk)-4):
                    if(kkk[j:j+5]=='"</b>'):
                        kkk=kkk[:j]+kkk[j+5:]
                        break
                bb=False
                bot.reply_to(message, kkk) 

                
def spearate_music(audio_name):
    try:
        os.system("conda activate team5")
        os.system(f"spleeter separate -p spleeter:2stems -o {audio_name}-output {audio_name}.mp3")
        return "OK"
    except:
        return "Fail"
                
                
@bot.message_handler(commands=['mp3'])
def send_mp3 (message):
    if message.chat.type in ("supergroup","private"):
        search_words = message.text[4:]
        try:
            yt = YouTube(findYT(search_words))
        except:
            bot.reply(message, "找不到或者有年齡限制")
        bot.reply_to(message,f"別催，已搜尋到 {yt.title}，處理中")
        audio_name = ''.join(random.choices(string.ascii_uppercase +string.digits, k=7))
        yt.streams.filter().get_audio_only().download(filename=f"{audio_name}.mp3")
        #儲存為mp3
        print(spearate_music(audio_name))
        bot.send_audio(chat_id=message.chat.id, title=f"{yt.title} - 伴奏", audio=open(f'{audio_name}-output/{audio_name}/accompaniment.wav', 'rb'))
        bot.send_audio(chat_id=message.chat.id, title=yt.title, audio=open(f'{audio_name}.mp3', 'rb'))

    
print("I'm online!")

bot.infinity_polling()
