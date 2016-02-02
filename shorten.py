import random
import string
from google.appengine.ext import ndb

class RedirectMap(ndb.Model):
    short = ndb.StringProperty()
    target = ndb.StringProperty()
    create_date = ndb.DateTimeProperty(auto_now_add=True)

# TODO: Don't allow a set of special URLs.
disallowed_keys = ["newUrl", "stats", "about", "list"]

key_chars = string.ascii_uppercase + string.ascii_lowercase + string.digits

def genRandKey():
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

def createShortRandom(target):
    """ Create a random short url given a target URL. """

    # TODO: Handle error conditions.
    # TODO: Limit number of attempts.

    max_attempts = 10

    for x in range(1, max_attempts):
        candidate=genRandKey()
        writeShort(candidate, str(target))
        if getTarget(candidate) == target:
            return candidate

    return "ERROR -- Handle this better.  Retries exceeded."


def writeShort(short, target):
    """ Store the association between key and target.  Will not overwrite
        a record so this is not appropriate for edit operations. """
    shortKey = ndb.Key(RedirectMap, short)

    # This get_or_insert strategy provides concurrency control.
    entry = RedirectMap().get_or_insert(short, short = short, target=target)

    if (entry.target != target):
        # TODO: Consider detecting here vs upstream.  The caller needs to
        # validate the target currently.
        pass

def getAll():
    # TODO: Limit & paginate this; it will break if there are too many entries.
    all_redirects = ndb.gql('SELECT * FROM RedirectMap')
    return all_redirects

def shortenTest():
    """ Simple test to validate the datastore doesn't duplicate keys """
    writeShort("abc", "First value")
    writeShort("abc", "Last value")

    return getTarget("abc")
