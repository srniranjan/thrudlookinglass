import webapp2
import logging
import os
import json

from google.appengine.ext.webapp import template
from model.prepared_data import PreparedData

def get_dict_for(concepts_by_date, time):
    for concept_by_date in concepts_by_date:
        if time == concept_by_date["date"]:
            return concept_by_date
    new_dict = {"date":time, "children":[]}
    concepts_by_date.append(new_dict)
    return new_dict

class VisualisationDataHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("Here..")
        concepts_by_date = []
        data = {"children" : concepts_by_date}
        q = PreparedData.all()
        q.filter("email =", self.request.get('email'))
        for concept in q.run(limit=1000):
            parent_dict = get_dict_for(concepts_by_date, concept.time)
            curr_dict = {
                    "name":concept.concept,
                    "occurances":concept.num_occurances,
                    "num_likes":concept.num_likes,
                    "len_text":concept.length
                    }
            parent_dict["children"].append(curr_dict)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(data))

app = webapp2.WSGIApplication([('/visualisation_data', VisualisationDataHandler)])
