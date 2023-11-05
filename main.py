import json
from dotenv import load_dotenv
import os
import base64
import requests
from requests import post, get
from azapi import *
api = AZlyrics()
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#Obtain Access Token

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials",
            "scope": "user-library-read user-library-modify user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-top-read user-read-playback-position user-read-recently-played user-follow-read user-follow-modify user-read-playback-state user-read-currently-playing user-modify-playback-state user-library-read user-library-modify user-read-playback-state user-read-currently-playing user-modify-playback-state playlist-read-collaborative playlist-modify-public playlist-modify-private ugc-image-upload"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

#Artist Search Function
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if (len(json_result) == 0):
        print("No artist exists with this name...")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
        headers = get_auth_header(token)
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["tracks"]
        return json_result


def get_recently_played(token, limit=10):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "limit": limit  # Specify the number of tracks to retrieve
    }
    try:
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            json_result = response.json()
            return json_result
        else:
            # Handle the error response from the API
            print(f"Failed to fetch recently played tracks. Status code: {response.status_code}")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {str(e)}")
        return None
     
AUTH_TOKEN = "AQCXOHIOgMkFVF-ywbFe5yODEgSMIFajbiQEWZnQforrylosiWgofO7Q3W_vmu4Yl1LLJeJ6M14c7LCcOw5xWXXw16PcIcTgmfjQVh2j0SHY18YGTE2qA9v7XFBo0mW9Mrs4gZeXWY1DWUZnERfdjm2M213Psk4b3NOW84LqoCcstSacntMQamZJUtrLcDYOTv6CEDA-temKk2AjkxkGphqy3cPyMMTzuRW2CTalQqQ6kERISfWKG0GqHtMDa9i5cC7suCNc2sh5jI6K638ZluRxbu-BpPJPPl7wuZlBLe__B1ZFEkoLkTdzm6fo2uh3TRz6tgjt4"
REFRESH_TOKEN = "AQDlEi-za7Kuz_N_v92Amtef6tzd_iH34IKTjJXvPbl_KaeXNxCUSXP4dLK0JTX92CXPbM1ky7rdZ4HxD_jF2_P8Ydu7tSds306sbTQVhgWxDGs8JEX2BJs3dENJQOWP6j8"
ACCESS_TOKEN = "BQDWRqNgcBTzuyzDpXXYuJSRSMnwgPOlYILPXxe3TJgDSm18dGpe0qktxZSDoP8_eSGPFDg0zD07-lCV1fjKm4fyMLj-hTALL4dJXXg7hPJRsyyi0_r_IeOS6qE_KX_MbJVuWzgoWZMoCtiWVBQmxGm3O2QiFC1XN_wsFAOPTXxufXMhP96w84UJ77kkUvv5SjXoRQRcWBZXzSfs5wmH338-sJLxKyTE4mS_MX7e5dVHa3HwqdcqfN6U750qNERjXJP790bCGp-4n-wPIXF95xwqe_WKrkWotS5IjDn3rQCaVlTfYfmLxpZEi-tYbMjSnszJNiuzCtaYp-g"

limit = 10
recently_played_tracks = get_recently_played(ACCESS_TOKEN, limit)
if recently_played_tracks:
    for item in recently_played_tracks.get("items", []):
        track_name = item.get("track", {}).get("name")
        artist_name = item.get("track", {}).get("artists", [{}])[0].get("name")
        print(f"Track: {track_name}, Artist: {artist_name}")

def make_recent_play_dictionary(recently_played_tracks):
    out = {}
    for item in recently_played_tracks.get("items", []):
        track_name = item.get("track", {}).get("name")
        artist_name = item.get("track", {}).get("artists", [{}])[0].get("name")
        out[artist_name] = track_name
    return out

songs = make_recent_play_dictionary(recently_played_tracks)

# for artist in songs:
#      api.artist = artist
#      api.title = songs[artist]

#      api.getLyrics(save=True, path="songs")

analyzer = SentimentIntensityAnalyzer()

folder_path = "songs"
list_song = []
if os.path.exists(folder_path) and os.path.isdir(folder_path):
    # Loop through the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            print(filename)
            print(folder_path+"/"+filename)
            with open(folder_path+"/"+filename, 'r') as file:
                text = file.read()
            sentiment = analyzer.polarity_scores(text)
            list_song.append(sentiment)

list_items = ""

# Loop through the dictionary and add the values to the list
for key, value in songs.items():
    list_items += f"<li>{value}, {key}</li>\n"

# Open the existing HTML file
with open('test.html', 'r') as file:
    existing_html = file.read()

# Find the location where you want to insert the generated content
insert_location = existing_html.find('</h2>')  # Insert after the closing </h1> tag

# Insert the generated content into the HTML
updated_html = existing_html[:insert_location] + f"<ul>{list_items}</ul>" + existing_html[insert_location:]

# Write the updated HTML content back to the file
with open('test.html', 'w') as file:
    file.write(updated_html)

print("Content added to the existing HTML file.")

pos = 0
neg = 0
neu = 0
print(list_song)
for song in list_song:
    for key in song:
        if(key == 'neg'):
            neg+=float(song[key])
        elif(key == 'pos'):
            pos+=float(song[key])
        else:
            neu+=float(song[key])

neu /= 10
categories = ['Negative', 'Neutral', 'Positive']

values = [neg, neu, pos]

# Create the bar graph
plt.bar(categories, values)

# Set the title
plt.title('Overall Sentiment')

plt.ylabel('Intensity Value of all 10 Songs')

# Save the chart as a PNG image
plt.savefig('bar_chart.png', format='png')
