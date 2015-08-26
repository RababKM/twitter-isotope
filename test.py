#!/usr/bin/env python

#system tools
import os, sys

#api tools
import requests, base64, json

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

'''
Consumer Key (API Key)	hcvgASeCyxkz4fGbsyA9yt9WD
Consumer Secret (API Secret)	bvSuLB49sVBlyu7jILbJU2IpRH8BqGmBy0ClZ48KpnLTKFJAsx
'''

CONSUMER_KEY = 'hcvgASeCyxkz4fGbsyA9yt9WD'
CONSUMER_SECRET = 'bvSuLB49sVBlyu7jILbJU2IpRH8BqGmBy0ClZ48KpnLTKFJAsx'

URL = 'https://api.twitter.com/oauth2/token'

credentials = base64.urlsafe_b64encode('%s:%s' % (CONSUMER_KEY, CONSUMER_SECRET))

custom_headers = {
            'Authorization': 'Basic %s' % (credentials),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
          }

grant_type_data = 'grant_type=client_credentials'

response = requests.post(URL, headers=custom_headers, data=grant_type_data)

print response
