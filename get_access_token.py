import requests

   # Replace with your actual Client ID and Client Secret
client_id = '5fx0c2tdp25zr3fuazhlqmwvezok4f'
client_secret =  'urarh94gbgbebzc0nmrnma0j4u1cmu'

   # Define the token endpoint and parameters
token_url = 'https://id.twitch.tv/oauth2/token'
params = {
       'client_id': '5fx0c2tdp25zr3fuazhlqmwvezok4f',
       'client_secret': 'urarh94gbgbebzc0nmrnma0j4u1cmu',
       'grant_type': 'client_credentials'  # This is the grant type for client credentials
   }

   # Send the POST request to get the access token
response = requests.post(token_url, params=params)

   # Check if the request was successful
if response.status_code == 200:
       token_data = response.json()
       access_token = token_data['access_token']
       print(f"Access Token: {access_token}")
else:
       print(f"Failed to obtain access token: {response.status_code} - {response.text}")