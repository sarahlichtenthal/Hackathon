import webbrowser

SPOTIFY_AUTH_URL= 'https://accounts.spotify.com/authorize'
SPOTIPY_CLIENT_ID = '7456bef01702477b9b133564bf1dd608'
SPOTIFY_SCOPES= 'user-library-read user-library-modify user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-top-read user-read-playback-position user-read-recently-played user-follow-read user-follow-modify user-read-playback-state user-read-currently-playing user-modify-playback-state user-library-read user-library-modify user-read-playback-state user-read-currently-playing user-modify-playback-state playlist-read-collaborative playlist-modify-public playlist-modify-private ugc-image-upload'


auth_url = (
    f"{SPOTIFY_AUTH_URL}?response_type=code&client_id={SPOTIPY_CLIENT_ID}"
    f"&scope={SPOTIFY_SCOPES}&redirect_uri=http://127.0.0.1:5000/redirect"
)

webbrowser.open(auth_url)