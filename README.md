# TFBot 1.0 - "Salute My Jorts" Edition
#### By Derpidoo@Github

## Objective

TFBot detects and automatically post new YouTube content to Reddit. 
It minimizes YouTube and Reddit API quota costs while requiring no 
persistent storage so as to remain easily containerized.

## Prerequisites

python 3.5 or later

yaml
praw
praw-OAuth2Util
google-api-python-client

## Configuration

TFBot is configured using a YAML file as show in this example:

```
---
subredditName: 'subreddit name'
channelId: 'youtube channel id' # channel name
minutesBetweenRun: 60 
youtube_developerKey: 'youtube api key'
reddit_clientId: 'reddit client id' # reddit client app name
reddit_clientSecret: 'reddit client api key'
reddit_username: 'reddit username'
reddit_password: 'reddit password'
```

## Usage

TFBot is intended to be run by a task scheduler. Cron would do
nicely. 

**NOTE**: Be sure to line up the `minutesBetweenRun` configuration
value with your task scheduler's settings!

Of course, it's also possible to run TFBot directly:

`python tfbot.py /path/to/config.yaml`
