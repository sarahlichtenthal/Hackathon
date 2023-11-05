from azapi import *

api = AZlyrics()

songs = {"Kanye West":"Praise God", "Rihanna":"S&M", "Lady Gaga":"Pokerface", "Justin Timberlake":"Mirrors", "Jack Harlow":"Dua Lipa", "ACDC":"Back in Black", "Yung Gravy":"Mr. Clean", "Eminem":"Rap God"}

for artist in songs:
    api.artist = artist
    api.title = songs[artist]

    api.getLyrics(save=True, path="songs")

    print(api.lyrics)

# Correct Artist and Title are updated from webpage
    print(api.title, api.artist)