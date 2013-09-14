import webapp2
import logging
import json
import urllib

from mapreduce import mapreduce_pipeline, base_handler
from google.appengine.api import urlfetch

from model.user import User

FACEBOOK_GRAPH_URL = 'https://graph.facebook.com/'
FQL_URL = "https://graph.facebook.com/method/fql?q=%s&format=json&access_token=%s"
STATUS_QUERY =  urllib.quote_plus("SELECT status FROM user WHERE uid=me()")

class PullFacebookData(base_handler.PipelineBase):
    def run(self):
        yield mapreduce_pipeline.MapreducePipeline(
            "facebook_date_pull",
            "facebook_date_pull_map",
            "facebook_date_pull_reduce",
            "mapreduce.input_readers.DatastoreInputReader",
            "mapreduce.output_writers.BlobstoreOutputWriter",
            mapper_params = {
                'entity_kind': User
            },
            reducer_params = {
                "mime_type":"text/plain"
            },
            shards = 16)
    
def facebook_data_pull_map(user):
    access_token = user.access_token
    response = json.loads(urlfetch.fetch(FQL_URL % (STATUS_QUERY, access_token), deadline=120).content)
    logging.info(response)

class PullFacebookDataHandler(webapp2.RequestHandler):
    def get(self):
        #pipeline = PullFacebookData()
        #pipeline.start()
        #self.redirect(pipeline.base_path + "/status?root=" + pipeline.pipeline_id)
        for user in User.all():
            params = {
                    'access_token': user.access_token,
                    'fields': 'statuses'
                    }
            response = json.loads(urlfetch.fetch(FACEBOOK_GRAPH_URL + user.id + '?' + urllib.urlencode(params)).content)
            logging.info(response)



app = webapp2.WSGIApplication([
                               ('/pull_facebook_data', PullFacebookDataHandler)
                               ])
