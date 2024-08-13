import json
import requests
import time
import re
import os


def get_credentials():
    with open('twitch_cred.json', 'r') as file:
        creds = json.load(file)
        uid = creds['client_id']
        secret = creds['client_secret']
        return uid, secret


def get_broadcaster_id(username, client_id, access_token):
    url = 'https://api.twitch.tv/helix/users'
    params = {'login': username}  # Username to search
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        if user_data['data']:
            user_id = user_data['data'][0]['id']
            return user_id
        else:
            print(f"No user found with username: {username}")
            return None
    else:
        print(f"Error fetching user data: {response.status_code}")
        if response.status_code == 429:
            check_rate_metrics(response)
        return None


def get_top_100_clip_data(client_id, broadcaster_id, access_token):
    clip_data = []
    url = f'https://api.twitch.tv/helix/clips?broadcaster_id={broadcaster_id}'

    headers = {
        'Client-Id': client_id,
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'first': 100,  # Get the top 100 clips
        'sort': 'views'  # Sorting by views gives you the top clips
    }

    response = requests.get(url, headers=headers, params=params)

    # Error Handling
    if response.status_code == 429:
        check_rate_metrics(response)
    elif response.status_code != 429 and response.status_code != 200:
        raise Exception(
            f'Failed to Create clip Mutually Exclusive to API Rates, Error Code {response.status_code}')

    clip_data = response.json()
    return clip_data['data']


def download_clip(filename, video_url, output_directory):
    response = requests.get(video_url)
    output_path = os.path.join(output_directory, filename)
    with open(output_path, 'wb') as vid:
        vid.write(response.content)


def check_rate_metrics(response):
    limit = response.headers.get('X-RateLimit')
    remaining = response.headers.get('X-RateLimit-Remaining')
    reset = response.headers.get('X-RateLimit-Reset')

    if limit and remaining and reset:
        limit = int(limit)
        remaining = int(remaining)
        reset_timestamp = int(reset)
        reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(reset_timestamp))

        print(f"Rate Limit: {limit}")
        print(f"Requests Remaining: {remaining}")
        print(f"Rate Limit Resets At: {reset_time} (UTC)")


def title_to_filename(title):
    filename = title.replace(' ', '_')

    filename = re.sub(r'[<>:"/\\|?*]', '', filename)

    filename = filename[:255]

    # add .mp4 to end of the filename
    return filename + ".mp4"
