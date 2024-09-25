import requests

def fetch_igdb_games():
    # Twitch API credentials
    client_id = '5fx0c2tdp25zr3fuazhlqmwvezok4f'
    access_token = '9xs6a5rq9q9i37q84ca5w82uasrwt9'

    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
    }

    url = 'https://api.igdb.com/v4/games'

    data = '''fields name, cover.url; 
              limit 50;'''  # Adjust the fields and limit as needed

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        games = response.json()
        return games
    else:
        return []

