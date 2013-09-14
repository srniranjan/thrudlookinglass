import json
import os
import webapp2
import logging
import urllib

from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch

from model.user import User

FB_APP_ID = '239096862911222'
FB_APP_SECRET = 'c3e176bb4c15aaef406d8d5f2cafba0c'
FB_REDIRECT_URI = 'http://thrudlookinglass.appspot.com/authenticate/facebook'

def get_fb_auth_url(email):
    params = {
            'client_id': FB_APP_ID,
            'redirect_uri': FB_REDIRECT_URI,
            'scope': '''email,user_status''',
            'state': email
            }
    url = 'https://www.facebook.com/dialog/oauth?' + urllib.urlencode(params)
    return url

def get_fb_token_url(email, code):
    params = {
            'client_id': FB_APP_ID,
            'client_secret': FB_APP_SECRET,
            'redirect_uri': FB_REDIRECT_URI,
            'code': code 
            }
    url = 'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(params)
    return url

class FacebookAuthenticateHandler(webapp2.RequestHandler):
    def get(self):
        code = self.request.get('code')
        email = self.request.get('state')
        response = urlfetch.fetch(get_fb_token_url(email, code))
        access_token = response.content.split('&')[0].split('=')[1]
        user_profile = json.loads(urlfetch.fetch('https://graph.facebook.com/me?access_token=' + access_token).content)
        user_object = User.get_or_insert(user_profile['email'], name=user_profile['name'], access_token=access_token)

app = webapp2.WSGIApplication([
                               ('/authenticate/facebook', FacebookAuthenticateHandler)
                               ])
