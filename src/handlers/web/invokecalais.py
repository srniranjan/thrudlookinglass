import webapp2
from mapreduce import mapreduce_pipeline, base_handler
from calais import Calais
from model.calais_results import CalaisResults
from google.appengine.ext import deferred

API_KEY = "4mq9g679ckr9ygudfppgxgaw"
calais = Calais(API_KEY, submitter="aiyappabeagles")

def calais_jobs_map(user_status):
    text = user_status.text
    time = user_status.time
    email = user_status.email
    to_process_text = text
    if len(text) > 99000:
        to_process_text = text[:99000]
    deferred.defer(analyze_with_calais, email, to_process_text, time, _queue="calaisanalyze")

def analyze_with_calais(email, text, timestamp):
    result = calais.analyze(text)
    calais_result = CalaisResults()
    calais_result.email = email
    calais_result.time = timestamp
    entity_names = []
    calais_result.result = result.print_entities()
    calais_result.put()

def calais_jobs_reduce():
    pass

class CalaisAnalyserPipeline(base_handler.PipelineBase):
    def run(self, email):
        yield mapreduce_pipeline.MapreducePipeline(
        "calais_jobs",
        "handlers.web.invokecalais.calais_jobs_map",
        "handlers.web.invokecalais.calais_jobs_reduce",
        "mapreduce.input_readers.DatastoreInputReader",
        "mapreduce.output_writers.BlobstoreOutputWriter",
        mapper_params = {
            "entity_kind":"model.user_status.UserStatus",
            "filters":[("email", "=", email)]
        },
        shards = 16)

class AnalyzeWithCalais(webapp2.RequestHandler): 
    def get(self):
        email = self.request.get('email')
        pipeline = CalaisAnalyserPipeline(email)
        pipeline.start()
        self.redirect(pipeline.base_path + "/status?root=" + pipeline.pipeline_id)

app = webapp2.WSGIApplication([('/analyze_with_calais', AnalyzeWithCalais)])
