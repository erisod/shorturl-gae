import random
import string
from google.appengine.ext import ndb

class RedirectMap(ndb.Model):
    short = ndb.StringProperty()
    target = ndb.StringProperty()
    create_date = ndb.DateTimeProperty(auto_now_add=True)

# TODO: Don't allow a set of special URLs.
disallowed_keys = ["newUrl", "stats", "about"]

key_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits

def genShortKey():
    """ Generate a candidate key. """
    key_length = 10
    return ''.join(random.SystemRandom().choice(key_chars) for _ in range(key_length))

def getTarget(short):
    """ Given a short url key return the target url or None if it 
      doesn't exist. """
    # redirect_record = RedirectMap.get_by_id(short)

    shortKey = ndb.Key(RedirectMap, short)

    # redirect_records = ndb.gql(
    #    'SELECT * FROM RedirectMap where short = :1', shortKey)

    redirect_record = shortKey.get()

    if redirect_record:
        return redirect_record.target
    else:
        return None

def createShort(target):
    """ Create a short url given a target URL. """

    # TODO: This needs concurrency control (gen key, check, write).
    # Find an unused short key.  TODO: Don't try forever.
    while True:
        candidate=genShortKey()
        if getTarget(candidate) is None:
            break

    writeShort(candidate, target)
    return candidate

def writeShort(short, target):
    """ Store the association between key and target. """
    shortKey = ndb.Key(RedirectMap, short)

    newUrl = RedirectMap()
    newUrl.key = shortKey
    newUrl.short = short
    newUrl.target = target
    newUrl.put()

def getAll():
    all = ndb.gql('SELECT * FROM RedirectMap')
    return all

def shortenTest():
    """ Simple test to validate desired key uniqueness behavior. """
    writeShort("abc", "xyz")
    writeShort("abc", "xyz2")

    return getTarget("abc")
