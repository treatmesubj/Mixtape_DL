import requests
from requests_html import HTML
import os
import re
from pprint import pprint
import win32api


print("https://www.datpiff.com/Big-Sean-Detroit-mixtape.390127.html")
link = input("datpiff mixtape link: ")

user_page = HTML(html=requests.get(link).text)
artist = user_page.find("li.artist", first=True).text
title = user_page.find("li.title", first=True).text

dir_loc = f"C:\\Users\\{win32api.GetUserName()}\\Music\\{artist}\\{title}"
if not os.path.exists(dir_loc):
	os.makedirs(dir_loc)

mixtape_code = link.split(".")[-2]
player_link = f"https://embeds.datpiff.com/mixtape/{mixtape_code}"
# player_html = HTML(html=requests.get(player_link).text)

# js = player_html.find("body>script")[-1].text
# pprint(js)

pl = requests.get(player_link).text

mfile_starts = [i.end() for i in re.finditer("mfile\":trackPrefix.concat", pl)]
mfile_ends = [i.end() for i in re.finditer(".mp3", pl)][1:]
mfiles = dict(zip(mfile_starts, mfile_ends))

song_links = [pl[key+3:val] for key,val in mfiles.items()]
pprint(song_links)


def substr(string, start_substr_substr, end_substr_substr):
	substr_start_index = string.find(start_substr_substr)
	substr_end_index = string[substr_start_index:].find(end_substr_substr) + substr_start_index
	return string[substr_start_index:substr_end_index]


base_url = substr(pl, "var trackPrefix", ";").split("'")[1]

headers = {
	"Host": "hw-mp3.datpiff.com",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
	"Accept": "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5",
	"Accept-Language": "en-US,en;q=0.5",
	"Range": "bytes=0-",
	"Connection": "keep-alive",
	"Referer": f"https://embeds.datpiff.com/mixtape/{mixtape_code}",
	"Pragma": "no-cache",
	"Cache-Control": "no-cache",
	"TE": "Trailers"
}

for song_link in song_links:

	full_link = f"{base_url}{song_link}"
	print(f"downloading {full_link}")

	try:
		
		with open(f"{dir_loc}\\{song_link}", "wb") as f:
			f.write(requests.get(f"{full_link}", headers=headers).content)
	
	except Exception as e:
		print(e)
		continue


input("done")
