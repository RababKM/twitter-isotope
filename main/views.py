from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
# Create your views here.

from main.models import Tweet

#system tools
import os, sys

#api tools
import requests, base64, json

#import Django's files tools
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

#unidecode helps django handle UTF-8
from unidecode import unidecode

def home(request):

    context = {}

    context['tweets'] = Tweet.objects.all()

    return render_to_response('home.html', context, context_instance=RequestContext(request))

def trending(request):

    context = {}

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

    #context['trending'] = response

    return JsonResponse(response.json(), safe=False)