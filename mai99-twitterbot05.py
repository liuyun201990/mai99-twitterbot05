import tweepy
import csv

print ('Loading mai99-twitterbot05 program...')

consumer_key = 'xxxxxxxxx'
consumer_secret = 'xxxxxxxxx'
access_token = 'xxxxxxxxx'
access_token_secret = 'xxxxxxxxx'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_all_tweets(screen_name):
#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name, count=200, tweet_mode='extended')
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ('Getting tweets before %s' % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name, count=200, max_id=oldest, tweet_mode='extended')
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("%s Tweets downloaded so far..." % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[("'"+str(tweet.id)), tweet.created_at, tweet.full_text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('%s tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["Tweets ID","Create At","Tweets"])
		writer.writerows(outtweets)
	pass

if __name__ == '__main__':
	#username of twitter account you want to download
	get_all_tweets("xxxxxxxxx")