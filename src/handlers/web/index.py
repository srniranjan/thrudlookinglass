import webapp2
import logging
import os

from google.appengine.ext.webapp import template

from handlers.web.authentication import get_fb_auth_url 

class VisualisationHandler(webapp2.RequestHandler):
    def get(self):
        index_path = os.path.join(os.path.dirname(__file__), '../../templates/visualise.html')
        vals = {
                'email':self.request.get("email")
                }
        self.response.out.write(template.render(index_path, vals))

class HomepageHandler(webapp2.RequestHandler):
    def get(self):
        email = ''
        template_values = { 'facebook_auth_url': get_fb_auth_url(email) }
        index_path = os.path.join(os.path.dirname(__file__), '../../templates/home.html')
        self.response.out.write(template.render(index_path, template_values))

app = webapp2.WSGIApplication([
                               ('/', HomepageHandler),
                               ('/visualise', VisualisationHandler)
                               ])
