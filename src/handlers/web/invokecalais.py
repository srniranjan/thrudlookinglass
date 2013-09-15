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
    result = calais.analyze(text.encode('utf-8'))
    calais_result = CalaisResults()
    calais_result.email = email
    calais_result.time = timestamp
    entity_names = []
    if result.get_entities():
        for entity in result.get_entities():
            entity_names.append(entity['name'])
    if result.get_topics():
        for topic in result.get_topics():
            entity_names.append(topic['categoryName'])
    calais_result.result = ' '.join(entity_names)
    calais_result.length = len(text)
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

def prepare_data_map(calais_result):
    if calais_result.result and len(calais_result.result.strip()) > 0:
        yield (time, result.split(' '))

def prepare_data_reduce(key, values):
    yield key + " : " + len(values) + "\n" 

class PrepareDataPipeline(base_handler.PipelineBase):
    def run(self, email):
        yield mapreduce_pipeline.MapreducePipeline(
        "prepare_data",
        "handlers.web.invokecalais.prepare_data_map",
        "handlers.web.invokecalais.prepare_data_reduce",
        "mapreduce.input_readers.DatastoreInputReader",
        "mapreduce.output_writers.BlobstoreOutputWriter",
        mapper_params = {
            "entity_kind":"model.calais_results.CalaisResults",
            "filters":[("email", "=", email)]
        },
        shards = 16)

class PrepareDataHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get('email')
        pipeline = PrepareDataPipeline(email)
        pipeline.start()
        self.redirect(pipeline.base_path + "/status?root=" + pipeline.pipeline_id)
        

app = webapp2.WSGIApplication([('/analyze_with_calais', AnalyzeWithCalais),
    ('/prepare_visualisation_data', PrepareDataHandler)])
