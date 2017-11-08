import sys
import string
import json
import twitter
import csv
from twython import Twython
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)

#FOR OAUTH AUTHENTICATION -- NEEDED TO ACCESS THE TWITTER API
t = Twython(app_key='', #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
    app_secret='',
    oauth_token='',
    oauth_token_secret='')


app_key='' #REPLACE 'APP_KEY' WITH YOUR APP KEY, ETC., IN THE NEXT 4 LINES
app_secret=''
oauth_token=''
oauth_token_secret=''


auth = OAuthHandler(app_key,app_secret)
api = tweepy.API(auth)
auth.set_access_token(oauth_token, oauth_token_secret)
twitterStream = Stream(auth,TweetListener())

outfn = 'data11.csv'
flag = False
outfp = open(outfn, 'wb')
outfp.close()

#User Id's should be inserted into this list
users1 = ['JayeshPatil1995', 'harshyadav2402']
for k in range(0,len(users1)):
    user = api.get_user(users1[k])
    ids = user.id
    users = t.lookup_user(user_id = ids)
    #field to be extracted
    fields = ['id', 'id_str', 'screen_name', 'location', 'description', 'url', 'followers_count', 'friends_count', 'listed_count', 'created_at', 'favourites_count', 'verified', 'statuses_count',\
              'lang', 'status', 'default_profile', 'default_profile_image', 'has_extended_profile', 'name']

    print (users)
    print ("\n\n\n\n\n");
    for entry in users:
        #CREATE EMPTY DICTIONARY
        r = {}
        for f in fields:
            r[f] = ""
        #ASSIGN VALUE OF ALL FIELDS IN JSON TO CERTAIN FIELD IN OUR DICTIONARY
        r['id'] = entry['id']
        r['id_str'] = entry['id_str']
        r['screen_name'] = entry['screen_name']
        r['location'] = entry['location']
        r['description'] = entry['description']
        r['url'] = entry['url']
        r['followers_count'] = entry['followers_count']
        r['friends_count'] = entry['friends_count']
        r['listed_count'] = entry['listed_count']
        r['created_at'] = entry['created_at']
        r['favourites_count'] = entry['favourites_count']
        r['verified'] = entry['verified']
        r['statuses_count'] = entry['statuses_count']
        r['lang'] = entry['lang']
        r['default_profile'] = entry['default_profile']
        r['default_profile_image'] = entry['default_profile_image']
        r['has_extended_profile'] = entry['has_extended_profile']
        r['name'] = entry['name']
        if 'status' in entry.keys():
            r['status'] = entry['status']
            print (r['status'])
            print ('\n\n\n\n')
        else:
            r['status'] = ""
            print ('\n\n\n\n')

        #NOT EVERY ID WILL HAVE A 'URL' KEY, SO CHECK FOR ITS EXISTENCE WITH IF CLAUSE
        if 'url' in entry['entities']:
            r['expanded_url'] = entry['entities']['url']['urls'][0]['expanded_url']
        else:
            r['expanded_url'] = ''
        print (r)
        print('\n\n\n')
        if flag is False:
            flag = True
            outfp = open(outfn, 'a')
            w = csv.DictWriter(outfp, r.keys())
            w.writeheader()
            w.writerow(r)

        else:
            flag = True

outfp.close()    
