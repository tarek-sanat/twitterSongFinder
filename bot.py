import tweepy
import json
import requests
import time
import os 
# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ['OAUTH_HANDLER'])
auth.set_access_token(os.environ['ACCESS_TOKEN'])

data = {
    'api_token': os.environ['API_TOKEN'],
    'url': '',
    'return': 'apple_music,spotify',
}
api = tweepy.API(auth)
	
#get id of the post
def getVidId(mention):
	tweet_id =mention._json
	return tweet_id["in_reply_to_status_id_str"]

#get url of MP4 video
def getVidUrl(twtId):
	public_tweets = api.get_status(str(twtId), tweet_mode='extended')
	tweets_json =public_tweets._json
	
	return tweets_json["extended_entities"]["media"][0]["video_info"]["variants"][0]["url"]

#get id of post to reply to
def getReplyId(mention):
	tweet_id = mention._json
	return tweet_id["id_str"]


#takes URL of MP4 and returns the title of the song
def getSongName(URL):
	data["url"] = URL
	result = requests.post('https://api.audd.io/', data=data)
	title = json.loads(result.text)["result"]["title"]
	artist = json.loads(result.text)["result"]["artist"]
	songName = title, artist
	return songName
	
	

def checkAtMe(since_id):
	newID = since_id
	for mentions in tweepy.Cursor(api.mentions_timeline, since_id = since_id).items():
		newID = max(mentions.id, newID)
		videoId = getVidId(mentions)
		videoUrl = getVidUrl(videoId)
		replyId = getReplyId(mentions)
		songName= getSongName(videoUrl)
		api.update_status(status= songName ,in_reply_to_status_id=mentions.id)
		if mentions.in_reply_to_status_id is not None:
            		continue
	return newID

#main func only fetches tweets once ever 5 seconds
def main():
	ID = 1
	while True:
		ID = checkAtMe(ID)   
		time.sleep(300)
	    
if __name__ == "__main__":
    main()