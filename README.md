# SITCONCamp2023-Team5-TGBot

## 安裝套件方法 Linux

```python
pip install -r requirements.txt 
```
## API Token 設定
- TMB.py Line 66
請找 @BotFather 拿取 Bot Token 後，輸入到這裡歐
```python
bot = telebot.TeleBot('填入你的Bot API Tokem')
```
## 執行
```
python TMB.py
```
## Spleeter 環境設定備用方案
```
conda install -c conda-forge ffmpeg libsndfile
pip install spleeter
```
## 參考資料

- 去人聲(音軌分離) https://github.com/deezer/spleeter
- TelegramBot機器人API https://github.com/eternnoir/pyTelegramBotAPI/tree/master/examples
- pyTelegramBotAPI 開發文件 https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.message_handler
