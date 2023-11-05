import base64
import requests

 # Replace with your actual credentials and the authorization code from the URL
SPOTIPY_CLIENT_ID = '7456bef01702477b9b133564bf1dd608'
SPOTIPY_CLIENT_SECRET = '636dbb0341f74ae489b672ad212dbbc7'
authorization_code = 'AQBq5frCOvuyk57D6vtDqIb87ABQkeRj_wLcK5g3E7T39YLnvBLYY58H0DBQuhN1No4kh8I6DooiRN6RWIoHgkuPdooWZR_yEFRklNhHUhT5i-U4JKLHs1cBmB1BFCsEPPZLzb25_yKJm4BAa2rZaRE0XBF-FBdDbGTj7NdYy_zyvcH3-nlFaR7358Q3YeUOI-cQuC0pckh864Ix3z17seL2Pe8etGET5nu-xXgJCzNv8LDQUqi6Ch6yKUmnda-qfzsSl8E0FawgDP44JN_HV9svxpBQUDtzi9o0UVLxjzRgu9uLF9W0ytrshJC0ztfWqaePtd4VfEMMHqZaYPsZYOhqx534eebBfCBPyLJassjAbaxEfph0T14078VvOlXxbmM9Z8vV_4MjRLdpTkVNoLWP4Ys__OUXRzXNk3ZozyjZUFKLyrWWEvH4JU4xa0glYIr-Zhwhahc-kLC06LNgxSfj_9JP1XmJKP6dATGuuEW5YhrYu2bj_LKlbm8hVe0ycS3LABQkouS17PqrRFuqIT2ZFqj0q600IC4mIQUcRJkPDmTGTeoLCjsT1OSwUfZBfzCpSEJhaeJ4tiaR6526rWowdfaZBIHZGkqNfHPkSR2gIPGZ0yaC4LdpQhrQZZjfSbJ5OpJXHJcx0UPeFDbGyH22MaSBXXRNie1oTEQOy4-9rMVhRg'  # Replace with the code from the URL

# Set up the data for the token request

token_url = 'https://accounts.spotify.com/api/token'
token_data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': 'http://127.0.0.1:5000/redirect',  # Must match the one used in the initial authorization request
}

# Create the authorization header
auth_header = base64.b64encode(f'{SPOTIPY_CLIENT_ID}:{SPOTIPY_CLIENT_SECRET}'.encode()).decode('utf-8')
# Set up headers
headers = {
    'Authorization': f'Basic {auth_header}',
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Make the POST request to exchange the code for tokens
response = requests.post(token_url, data=token_data, headers=headers)
if response.status_code == 200:

    token_info = response.json()

    access_token = token_info['access_token']

    refresh_token = token_info['refresh_token']

    print(f'Access Token: {access_token}')

    print(f'Refresh Token: {refresh_token}')

else:

    print(f'Error: {response.status_code}')