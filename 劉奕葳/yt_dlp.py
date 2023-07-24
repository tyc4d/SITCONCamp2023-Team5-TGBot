# import os
from os import system
import yt_dlp

url = "https://www.youtube.com/watch?v=6LpFPXJ7-AI"

system(f"rm output.mp3")
system(f"yt-dlp -f 'ba' -x --audio-format mp3 {url} -o output.mp3")
system(f"spleeter separate -p spleeter:2stems -o spleeter {'oxxostudio.mp3'}")