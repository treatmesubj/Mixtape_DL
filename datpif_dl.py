import requests
from requests_html import HTML
import os
import re
from pprint import pprint

# link = input("datpiff mixtape link: ")
link = "https://www.datpiff.com/Big-Sean-Detroit-mixtape.390127.html"

user_page = HTML(html=requests.get(link).text)
artist = user_page.find("li.artist", first=True).text
title = user_page.find("li.title", first=True).text

dir_loc = f"C:\\Users\\jrock\\Music\\{artist}\\{title}"
if not os.path.exists(dir_loc):
	os.makedirs(dir_loc)

mixtape_code = link.split(".")[-2]
player_link = f"https://embeds.datpiff.com/mixtape/{mixtape_code}"
player_html = HTML(html=requests.get(player_link).text)

js = player_html.find("body>script")[-1].text
pprint(js)

mfile_starts = [i.end() for i in re.finditer("mfile\":trackPrefix.concat", js)]
mfile_ends = [i.end() for i in re.finditer(".mp3", js)][1:]
mfiles = dict(zip(mfile_starts, mfile_ends))

song_links = [js[key+3:val] for key,val in mfiles.items()]
pprint(song_links)

def substr(string, start_substr_substr, end_substr_substr):
	substr_start_index = string.find(start_substr_substr)
	substr_end_index = string[substr_start_index:].find(end_substr_substr) + substr_start_index
	return string[substr_start_index:substr_end_index]


base_url = substr(js, "var trackPrefix", ";").split("'")[1]

for song_link in song_links:
	try:

		full_link = f"{base_url}{song_link}"
		print(full_link)

		with open(f"{dir_loc}\\{song_link}", "wb") as f:
			f.write(requests.get(f"{base_url}{song_link}").content)

	except Exception as e:
		print(e)
		breakpoint()

input("done")

playerData.tracks[0].mfile