#!/usr/bin/env python

#system tools
import os, sys

#api tools
import requests, base64, json

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from main.models import Tweet

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from unidecode import unidecode


'''
Consumer Key (API Key)	hcvgASeCyxkz4fGbsyA9yt9WD
Consumer Secret (API Secret)	bvSuLB49sVBlyu7jILbJU2IpRH8BqGmBy0ClZ48KpnLTKFJAsx
'''

CONSUMER_KEY = 'hcvgASeCyxkz4fGbsyA9yt9WD'
CONSUMER_SECRET = 'bvSuLB49sVBlyu7jILbJU2IpRH8BqGmBy0ClZ48KpnLTKFJAsx'

URL = 'https://api.twitter.com/oauth2/token'

SEARCH_TERM = 'techcrunch'

credentials = base64.urlsafe_b64encode('%s:%s' % (CONSUMER_KEY, CONSUMER_SECRET))

custom_headers = {
                    'Authorization': 'Basic %s' % (credentials),
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                 }

grant_type_data = 'grant_type=client_credentials'

#passing custom headers and grant type to https://api.twitter.com/oauth2/token to get a authentication token
response = requests.post(URL, headers=custom_headers, data=grant_type_data)

#getting access token out of the dictionary sent from twitter
access_token = response.json().get('access_token')

#setting headers to use the access token retrieved from twitter
search_headers = {'Authorization': 'Bearer %s' % (access_token), }

#querying the twitter servers with the access token in the headers
#response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q=place%3AKuwait%3A2', headers=search_headers)
response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q=%s' % SEARCH_TERM, headers=search_headers)


count = response.json().get('search_metadata').get('count')

#print response.json()['statuses'][0]['tweet_text']
#print response.json().get('statuses')[0].get('tweet_text')

# if response.json().get('statuses')[0].get('tweet_text') != None:
#     print 'text 1 found'
# else:
#     print 'text1 was not found'

#print response.json().get('statuses')[0].get('text')

tweet_list = response.json().get('statuses')
i = 0

for tweet in tweet_list:
    #if tweet.get('geo') != None:
    #print tweet.keys()
    #print tweet.get('user').keys()
    image_url = tweet.get('user').get('profile_image_url_https')
    twitter_user = tweet.get('user').get('screen_name')
    tweet_text = tweet.get('text')

    new_tweet = Tweet.objects.create(text=unidecode(tweet_text))
    new_tweet.user = twitter_user
    new_tweet.search = SEARCH_TERM

    temp_image = NamedTemporaryFile(delete=True)
    image_link = requests.get(image_url)
    temp_image.write(image_link.content)

    filename = "tweetimage_%s" % i

    new_tweet.image.save(filename, File(temp_image))

    new_tweet.save()

    i+1





#response = requests.get('https://api.twitter.com/1.1/trends/place.json?id=1', headers=search_headers)

#print response.json()