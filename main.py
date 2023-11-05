import json
from dotenv import load_dotenv
import os
import base64
import requests
from requests import post, get
import webbrowser
from azapi import *
api = AZlyrics()

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
REFRESH_TOKEN = "AQDDUwyH-lXPNfx49vB1UDTzvwoJaktlzgSdzO4ZD5PSr-8xX0I9v5dqmeM8cjbXlMQk6T5t8WnRRWTGlrvlvequzQ82jQDW5z4i_YbppAxH6u7rG6MhTeC5-ga9_kKm1p4"
ACCESS_TOKEN = "BQBm2qxBPG0rf62Pxd8STT9DmtFzCqzZK0dl7fYpDQAjyklspMbIml439Q_f33igS3XM8i2qr-7tlDZzhXnd3qQC6ckPsCIMhHPUFoF111XgD6WFfaxYe2s_4VGXQhAZVhrHDD6QeNHirICBqRW_rzs4pqd83-4NrQb9zjJj_bEAPGKGLdxAlJICJn3JeWbZNNDUSm5Cw083dOmROuWUSnAvFzcrV4ZDLP8RonwQVe9Nw4OYKuFRIApKiklOzlnw1AX6ntGd29g0A2Eh-o4vdFWVhk98PyUAhe54eXmRVRHaasB_f9f7LevvtzYYzu0"
# Replace with your actual credentials and the authorization code from the URL

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

print(make_recent_play_dictionary(recently_played_tracks))

songs = make_recent_play_dictionary(recently_played_tracks)

# for artist in songs:
#     print(artist+",'"+songs[artist]+"'")


for artist in songs:
    api.artist = artist
    api.title = songs[artist]

    api.getLyrics(save=True)

    print(api.lyrics)
    print(api.title, api.artist)