import webapp2
import logging
import json
import urllib

from mapreduce import mapreduce_pipeline, base_handler
from google.appengine.api import urlfetch
from google.appengine.ext import deferred

from model.user import User
from model.user_status import UserStatus
from datetime import datetime

FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/'

def get_month_year(time_stamp):
    format_str = '%Y-%m-%d'
    time_object = datetime.strptime(time_stamp.split('T')[0], format_str)
    return datetime.strftime(time_object, '%m:%Y')

def pull_statuses(email, url):
    response = urlfetch.fetch(url, deadline=120)
    result = json.loads(response.content)
    if result and 'paging' in result and 'next' in result['paging']:
        deferred.defer(pull_statuses, email, result['paging']['next'])
    if 'data' in result:
        for status in result['data']:
            if 'message' in status:
                text = []
                text.append(status['message'])
                time = get_month_year(status['updated_time'])
                if 'comments' in status:
                    for comment in status['comments']['data']:
                        text.append(comment['message'])
                user_status = UserStatus()
                user_status.text = '. '.join(text)
                user_status.email = email
                user_status.time = time
                user_status.put()

class PullFacebookDataHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get('email')
        user = User.get_by_key_name(email)
        url = FACEBOOK_GRAPH_URL + 'me/statuses?access_token=' + user.access_token
        deferred.defer(pull_statuses, email, url)

app = webapp2.WSGIApplication([
                               ('/pull_facebook_data', PullFacebookDataHandler)
                               ])
