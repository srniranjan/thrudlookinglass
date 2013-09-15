from google.appengine.ext import db

class CalaisResults(db.Model):
    email = db.StringProperty()
    time = db.StringProperty()
    result = db.TextProperty(indexed=False)
    length = db.IntegerProperty(indexed=False)
