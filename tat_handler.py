# Twitch Access Token (TAT) Handler


import time
import requests


def validate_token(client_id, access_token):
    validation_url = 'https://id.twitch.tv/oauth2/validate'
    params = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(validation_url, params=params)

    if response.status_code == 401:
        print("Invalid: Access Token Expired")
        return False

    elif response.status_code == 200:
        expiration_time = time.time() + response.json()['expires_in']
        print("Token is Still Valid: Time to Expire", expiration_time)
        return True


# get_access_token returns the TwitchAPI access token, refresh_token
# and expiration time, given a client_id and client_secret
def get_access_token(client_id, client_secret):
    token_url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(token_url, params=params)

    # Error Handling
    if response.status_code != 429 and response.status_code != 200:
        raise Exception('Connectivity Issue Mutually Exclusive to API Rates')
    elif response.status_code == 200:
        token_data = response.json()
        print(token_data)
        access_token = token_data['access_token']
        expires_in = token_data['expires_in']  # Token expiry in seconds
        expiration_time = time.time() + expires_in
        return access_token, expiration_time



