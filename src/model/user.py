from google.appengine.ext import db

class User(db.Model):
    email = db.StringProperty()
    access_token = db.StringProperty(indexed=False)

    @classmethod                                                                                                                                                                 
    def get_or_insert(cls, key_name, **kwds):
        kwds['email'] = key_name
        return super(User, cls).get_or_insert(key_name, **kwds)
   
    def update_access_token(self, access_token):
        self.access_token = access_token
        self.put()
