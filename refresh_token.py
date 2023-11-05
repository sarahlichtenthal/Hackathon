import base64
import requests

 # Replace with your actual credentials and the authorization code from the URL
SPOTIPY_CLIENT_ID = '7456bef01702477b9b133564bf1dd608'
SPOTIPY_CLIENT_SECRET = '636dbb0341f74ae489b672ad212dbbc7'
authorization_code = 'AQCPw32mYC0l4VIux59CpMVziMvW7X9p8nkXZa2eGGjSCY2uVuRjaqkr9WNSV1-7D7W30DLJVMBxB4i7rJ2mr0YwA1ufjJpN9m1XUdK7K3Yf_bWDSRUj0mi12XERYG4JVGSk983xrTTqYQIaPwMro1hV9xSoLI__IgHgWjJ3L81m6F6GQCdV5SyftUfThantuZF7YBnEJIyaeaz7DSvJDNx5CIv6v3HaSJ-SfG-8xPz8fAdAFRra9ggkz04Vrpd5lqMvIQDiepMPSgeRaKVVplC7gdn2MQxsQIRBuR0Ap6MGayuMeOLPvJV3Bo_hZt5M_5lHR7kuYhENf8bIQ6O6wzhIYcvrcvuIyi1bMxh4BmZeJikWZbpxq8cuP1YJ5Fr-Nx-pG-tef99nvZElPdErykWNIOsKxuWjPFAWuOT6pi2nSoIGQycthNuEWNU6ydxsMAClcDTa4eJC404gHQKD13aXT_6llSsV6QnXte68-gMeIS_BjAJ2MTYi6dRwbdZ616qfZ0JGYyO311Uktdj2_gP-Q-a6uV8BdUBcKoadIpDD26AwCYKuiypiISK4rEBBeO4katwe8aM6RMqLLHN8Rdy_SE3BkmcsuWv8o6cgXXrSIupraDN47DtaXdnePHMR_iDa5P4gbsD5NMsU2hTC6zJg0DVE78GrcZ4RVPaQhI0CbY70Xg'  # Replace with the code from the URL

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