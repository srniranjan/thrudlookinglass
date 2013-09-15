from google.appengine.ext import db

class PreparedData(db.Model):
    email = db.StringProperty()
    time = db.StringProperty()
    entity = db.StringProperty(indexed=False)
    num_occurances = db.IntegerProperty(indexed=False)
    num_likes = db.IntegerProperty(indexed=False)
    length = db.IntegerProperty(indexed=False)
