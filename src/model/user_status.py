from google.appengine.ext import db

class UserStatus(db.Model):
    email = db.StringProperty()
    text = db.TextProperty(indexed=False)
    time = db.StringProperty()
