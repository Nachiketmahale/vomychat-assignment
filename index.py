import requests
from googleapiclient.discovery import build
from TikTokApi import TikTokApi

# API Key for YouTube
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"
# Instagram and Facebook access token (required for API access)
INSTAGRAM_ACCESS_TOKEN = "YOUR_INSTAGRAM_ACCESS_TOKEN"
FACEBOOK_ACCESS_TOKEN = "YOUR_FACEBOOK_ACCESS_TOKEN"

# Initialize TikTok API
tiktok_api = TikTokApi.get_instance()

# YouTube API Setup
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Function to detect if URL is a homepage or post and scrape data
def scrape_data(url):
    if "youtube.com" in url:
        if "watch" in url:
            video_id = url.split("v=")[-1]
            get_youtube_video_comments(video_id)
        elif "channel" in url or "c/" in url:
            channel_name = url.split("/")[-1]
            get_youtube_channel_data(channel_name)

    elif "instagram.com" in url:
        if "/p/" in url:
            post_id = url.split("/p/")[-1].split("/")[0]
            get_instagram_post_comments(post_id)
        else:
            username = url.split("instagram.com/")[-1].strip("/")
            get_instagram_data(username)

    elif "tiktok.com" in url:
        if "/video/" in url:
            video_id = url.split("/video/")[-1]
            get_tiktok_video_comments(video_id)
        else:
            username = url.split("/@")[-1]
            get_tiktok_user_data(username)

    elif "facebook.com" in url:
        if "/posts/" in url:
            post_id = url.split("/posts/")[-1]
            get_facebook_post_comments(post_id)
        else:
            username = url.split("facebook.com/")[-1].strip("/")
            get_facebook_user_data(username)

# ------------------------ YouTube ------------------------

def get_youtube_channel_data(channel_name):
    print("\nWhat would you like to scrape from this YouTube channel?")
    choice = input("Type 'followers' to scrape subscribers data or 'following' to scrape following data: ").strip().lower()

    if choice == "followers":
        request = youtube.channels().list(part="snippet,statistics", forUsername=channel_name)
        response = request.execute()

        if response['items']:
            channel = response['items'][0]
            print(f"Channel Name: {channel['snippet']['title']}")
            print(f"Subscribers: {channel['statistics']['subscriberCount']}")
        else:
            print("No channel found.")

    elif choice == "following":
        print("YouTube does not expose following data publicly through the API.")
    
    else:
        print("Invalid choice. Please type 'followers' or 'following'.")

def get_youtube_video_comments(video_id):
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=5)
    response = request.execute()
    
    if response.get("items"):
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            print(f"Comment by {comment['authorDisplayName']}: {comment['textDisplay']}")
    else:
        print("No comments found.")

# ------------------------ Instagram ------------------------

def get_instagram_data(username):
    print("\nWhat would you like to scrape from this Instagram profile?")
    choice = input("Type 'followers' to scrape followers data or 'following' to scrape following data: ").strip().lower()

    if choice == "followers":
        url = f"https://graph.instagram.com/{username}?fields=id,username,followers_count&access_token={INSTAGRAM_ACCESS_TOKEN}"
        response = requests.get(url).json()
        print(f"Instagram Username: {response['username']}")
        print(f"Followers: {response['followers_count']}")

    elif choice == "following":
        url = f"https://graph.instagram.com/{username}?fields=id,username,follows_count&access_token={INSTAGRAM_ACCESS_TOKEN}"
        response = requests.get(url).json()
        print(f"Instagram Username: {response['username']}")
        print(f"Following: {response['follows_count']}")

    else:
        print("Invalid choice. Please type 'followers' or 'following'.")

def get_instagram_post_comments(post_id):
    url = f"https://graph.instagram.com/{post_id}/comments?access_token={INSTAGRAM_ACCESS_TOKEN}"
    response = requests.get(url).json()
    
    if response.get('data'):
        for comment in response['data']:
            print(f"Comment: {comment['text']} by {comment['username']}")
    else:
        print("No comments found.")

# ------------------------ TikTok ------------------------

def get_tiktok_user_data(username):
    print("\nWhat would you like to scrape from this TikTok profile?")
    choice = input("Type 'followers' to scrape followers data or 'following' to scrape following data: ").strip().lower()

    if choice == "followers":
        user = tiktok_api.get_user(username)
        print(f"TikTok Username: {user['user_info']['user']['nickname']}")
        print(f"Followers: {user['user_info']['stats']['followerCount']}")
    elif choice == "following":
        user = tiktok_api.get_user(username)
        print(f"TikTok Username: {user['user_info']['user']['nickname']}")
        print(f"Following: {user['user_info']['stats']['followingCount']}")
    else:
        print("Invalid choice. Please type 'followers' or 'following'.")

def get_tiktok_video_comments(video_id):
    video = tiktok_api.get_video_by_id(video_id)
    comments = video['comments']
    
    for comment in comments:
        print(f"Comment: {comment['text']} by {comment['author']['nickname']}")

# ------------------------ Facebook ------------------------

def get_facebook_user_data(username):
    print("\nWhat would you like to scrape from this Facebook profile?")
    choice = input("Type 'followers' to scrape followers data or 'following' to scrape following data: ").strip().lower()

    if choice == "followers":
        url = f"https://graph.facebook.com/{username}?fields=id,name,followers_count&access_token={FACEBOOK_ACCESS_TOKEN}"
        response = requests.get(url).json()
        print(f"Facebook Username: {response['name']}")
        print(f"Followers: {response.get('followers_count', 'N/A')}")

    elif choice == "following":
        print("Facebook does not expose following data publicly through the API.")

    else:
        print("Invalid choice. Please type 'followers' or 'following'.")

def get_facebook_post_comments(post_id):
    url = f"https://graph.facebook.com/{post_id}/comments?access_token={FACEBOOK_ACCESS_TOKEN}"
    response = requests.get(url).json()
    
    if response.get('data'):
        for comment in response['data']:
            print(f"Comment: {comment['message']} by {comment['from']['name']}")
    else:
        print("No comments found.")

# ------------------------ Example Usage ------------------------

# Test URLs for homepage or post detection
scrape_data("https://www.youtube.com/c/username")  # Homepage URL (Channel)
scrape_data("https://www.youtube.com/watch?v=video_id")  # Post URL (Video)
scrape_data("https://www.instagram.com/username/")  # Homepage URL (Profile)
scrape_data("https://www.instagram.com/p/post_id/")  # Post URL (Post)
scrape_data("https://www.tiktok.com/@username/")  # Homepage URL (Profile)
scrape_data("https://www.tiktok.com/@username/video/video_id")  # Post URL (Video)
scrape_data("https://www.facebook.com/username")  # Homepage URL (Profile)
scrape_data("https://www.facebook.com/post_id")  # Post URL (Post)
