# monolithic build script
# I'm really trying I promise

import os
import pystache
import json
import shutil

# KILL
shutil.rmtree("dist", ignore_errors=True)

os.makedirs("dist/music", exist_ok=True)

# lol
shutil.copyfile("site/index.html", "dist/index.html")
shutil.copyfile("site/404.html", "dist/404.html")
shutil.copyfile("site/CNAME", "dist/CNAME")

shutil.copytree("site/assets", "dist/assets")
shutil.copytree("site/.well-known/", "dist/.well-known/")

with open("site/music/index.mustache", "r") as file:
	music_template = file.read()

with open("dist/music/index.html", "w") as file:	
	with open("site/music/entries.json", "r") as data:
		entries = json.load(data)

		entries.sort(key=lambda entry: entry["date"], reverse=True)
		
		years = []
		entries_by_year = []
		for entry in entries:
			year = int(entry["date"].split("-")[0])
			if year not in years:
				years.append(year)
				entries_by_year.append({"year": year, "entries": []})
		
		for entry in entries:
			year = int(entry['date'].split('-')[0])
			entries_by_year[years.index(year)]["entries"].append(entry)

		print(entries_by_year)

		file.write(
			pystache.render(music_template, {"entries": entries_by_year})
		)

# get the music files where they need to go
shutil.copytree("site/music/files", "dist/music/files")
