#!/usr/bin/env python3
import time
import datetime
import argparse
import yaml
import praw # reddit
import OAuth2Util # reddit oauth
import googleapiclient.discovery # google api
import googleapiclient.errors # google api

version = "TFBot 1.0"
parser = argparse.ArgumentParser(description=version)
parser.add_argument('configfile', type=argparse.FileType('r'))
args = parser.parse_args()
cfg = yaml.load(args.configfile)

def main():
    videos = fetchrecentvideos()
    addredditposts(videos)

def addredditposts(videos):
    # Create a reddit object
    reddit = praw.Reddit(client_id=cfg['reddit_clientId'],
                         client_secret=cfg['reddit_clientSecret'],
                         username=cfg['reddit_username'],
                         password=cfg['reddit_password'],
                         user_agent=version)
    for video in videos:
        print("posting to reddit: " + 'https://youtu.be/'+video) 
        try:
            reddit.subreddit(cfg['subredditName']).submit(videos[video], url='https://youtu.be/'+video)
        except Exception as e:
            print(e)
            exit(255)
        print("posted to reddit: " + 'https://youtu.be/'+video) 

def fetchrecentvideos():
    current_utc = datetime.datetime.utcnow()
    delta_utc = current_utc - datetime.timedelta(minutes=cfg['minutesBetweenRun'])
    # Do the needful setup for YT's API
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    api_service_name = "youtube"
    api_version = "v3"
    for x in range(1,5):    # youtube likes to ignore us sometimes
        try: 
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey=cfg['youtube_developerKey'])
        except:
            time.sleep(5)
            continue
        break
    else:
        print("YouTube didn't answer after 5 tries, giving up...")
        exit(254)

    # Request from YT's API
    request = youtube.activities().list(
        part="snippet, contentDetails", # API quota cost will be 4 per line item, 2 each for these properties
        channelId=cfg['channelId'],
        maxResults=22, # this is probably higher than it needs to be, but shouldn't matter because of the next bit
        publishedAfter=str(delta_utc.isoformat()+'Z') # try to minimize our API quota impact
    )
    response = request.execute()
    # Parse the response dictionary into results we care about
    result={}
    for item in response.get('items'):
        if (item['snippet']['type'] != 'upload'):
            continue # Skip activity types that aren't uploads (although playlistItem shows up hours sooner...)
        result[item['contentDetails']['upload']['videoId']] = item['snippet']['title']
        print("Found video " + item['contentDetails']['upload']['videoId'])
    try:
        return result
    except UnboundLocalError: # we got no videos to return
        exit()

if __name__ == "__main__":
    main()
