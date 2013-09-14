from google.appengine.ext import db

class User(db.Model):
    email = db.StringProperty()
    name = db.StringProperty(indexed=False)
    access_token = db.StringProperty(indexed=False)

    @classmethod                                                                                                                                                                 
    def get_or_insert(cls, key_name, **kwds):
        kwds['email'] = key_name
        return super(User, cls).get_or_insert(key_name, **kwds)
   
