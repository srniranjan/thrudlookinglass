import webapp2
import logging
import os
import json

from google.appengine.ext.webapp import template
from data.test_data import data

class VisualisationDataHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(data))

app = webapp2.WSGIApplication([('/visualisation_data', VisualisationDataHandler)])
