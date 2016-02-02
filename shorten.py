import random
import string
from google.appengine.ext import ndb

class Redirect(ndb.Model):
    short = ndb.StringProperty()
    target = ndb.StringProperty()
    create_date = ndb.DateTimeProperty(auto_now_add=True)

# TODO: Don't allow a set of special URLs.
disallowed_keys = ["newUrl", "stats", "about"]

def genShortKey(self):
    """ Generate a candidate key. """
    key_length = 10
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(key_length))

def getTarget(self, short):
    """ Given a short url key return the target url or None. """

    redirect_record = Redirect.get_by_id(short)

    if redirect_record:
        # TODO: Don't limit to 1 result and throw an error if we see >1.
        return redirect_record[0].target
    else:
        return None

def createShort(self, target):
    """ Create a short url given a target URL. """

    # Find an unused short key.  TODO: Don't try forever.
    while True:
        candidate=self.genShortKey()
        if self.getTarget(candidate) is None:
            break

    self.writeShort(candidate, target)
    return candidate

def writeShort(self, key, target):
    """ Store the association between key and target. """
    newUrl = Redirect()
    newUrl.short = key
    newUrl.id = key
    newUrl.target = target
    newUrl.put()

def getAll(self):
    all = ndb.gql('SELECT * FROM Redirect LIMIT 100')
    print all
