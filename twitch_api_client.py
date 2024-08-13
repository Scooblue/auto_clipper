import twitch_utils as tu
from auto_clipper import tat_handler as tat

output_directory = '/home/declancoleman/Documents/GitHub/auto_clipper/clips'
top_100_clips = []
urls = []
cleaned_titles = []

# uid is your applications client_id on twitch developer page
# secret is your applications client_secret on twitch developer page

uid, secret = tu.get_credentials()

# at = access token
# exp = expiration time

at, exp = tat.get_access_token(uid, secret)

username = input("Please enter a valid username of streamer you would like to clip: ")
print(username)
bid = tu.get_broadcaster_id(username, uid, at)
while not bid:
    username = input("Please enter a valid username of streamer you would like to clip: ")
    bid = tu.get_broadcaster_id(username, uid, at)

# token validation according to twitch api policy
# access tokens must be validated every 60 minutes

top_100_clips = tu.get_top_100_clip_data(uid, bid, at)
for clip in top_100_clips:
    urls.append(clip['url'])
    cleaned_titles.append(tu.title_to_filename(clip['title']))
    print(f"Clip Title: {clip['title']}, URL: {clip['url']}")

print(f"Total number of clips urls: {len(urls)}")

for title, url in zip(cleaned_titles, urls):
    tu.download_clip(title, url, output_directory)





