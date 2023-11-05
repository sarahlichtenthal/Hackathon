import azapi 

API = azapi.AZlyrics('google', accuracy=0.5)

API.artist = 'Kanye West'
API.title = 'Flashing Lights'

API.getLyrics(save=True, ext='lrc')

print(API.lyrics)

# Correct Artist and Title are updated from webpage
print(API.title, API.artist)