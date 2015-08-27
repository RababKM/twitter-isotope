#!/usr/bin/env python

#system tools
import os, sys

#api tools
import requests, base64, json

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

#import models
from main.models import Tweet

#import Django's files tools
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

#unidecode helps django handle UTF-8
from unidecode import unidecode

#the twitter app api keys that are used to authenticate you with django
CONSUMER_KEY = 'hcvgASeCyxkz4fGbsyA9yt9WD'
CONSUMER_SECRET = 'bvSuLB49sVBlyu7jILbJU2IpRH8BqGmBy0ClZ48KpnLTKFJAsx'

#the base twitter url for sending api requests
URL = 'https://api.twitter.com/oauth2/token'

#the search term to be used
SEARCH_TERM = 'techcrunch'

#the twitter api keys being encoded into a format twitter will like
credentials = base64.urlsafe_b64encode('%s:%s' % (CONSUMER_KEY, CONSUMER_SECRET))

#the custom headers that contain the formatted api keys
custom_headers = {
                    'Authorization': 'Basic %s' % (credentials),
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                 }

#post variable declaring the type of authentication or 'grant type' being used
grant_type_data = 'grant_type=client_credentials'

#sending a post request to the base twitter URL with the custom headers and post variable
response = requests.post(URL, headers=custom_headers, data=grant_type_data)

#the response that contains the access token
access_token = response.json().get('access_token')

#new custom header that passes the access token to twitter
search_headers = {'Authorization': 'Bearer %s' % (access_token), }

#sending a get request to the twitter search api url with the search term and search headers
response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q=%s' % SEARCH_TERM, headers=search_headers)

#the number of tweets received
count = response.json().get('search_metadata').get('count')

#a list of tweets
tweet_list = response.json().get('statuses')

i = 0
#looping though each tweet, creating a new "Tweet" object, and saving it
for tweet in tweet_list:

    #creating the "Tweet" object
    image_url = tweet.get('user').get('profile_image_url_https')

    #getting the username and tweet text out of the tweet from the tweet list
    twitter_user = tweet.get('user').get('screen_name')
    tweet_text = tweet.get('text')

    #setting the user, text and search term attributes on the "Tweet" object
    new_tweet = Tweet.objects.create(text=unidecode(tweet_text))
    new_tweet.user = twitter_user
    new_tweet.search = SEARCH_TERM

    #creating a temporary 'in memory' file to stream the twitter image into
    temp_image = NamedTemporaryFile(delete=True)

    #getting the image file/data from the twitter server
    image_link = requests.get(image_url)

    #writing the file/data from the twitter server to the temporary file
    temp_image.write(image_link.content)

    #naming the file
    filename = "tweetimage_%s.jpg" % i

    #saving the "Tweet" object to the database
    new_tweet.image.save(filename, File(temp_image))
    i+1