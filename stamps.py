"""Load and save etags from RSS feeds."""
import os
from dbco import db
from datetime import datetime

def loadLastStamp(name):
    """Load a timestamp from a RSS feed name.

    This name should be consistent with `saveLastStamp`.

    Arguments:
    name -- The name of the feed used to save the timestamp.
    """
    path = 'stamps/'+name+'.txt'
    if os.path.isfile(path):
        with open(path) as f:
            txt = f.read()
            return float(txt)
    return 0

def saveLastStamp(name, stamp):
    """Save a timestamp from an RSS feed for later.

    This name should be consistent with `loadLastStamp`.

    Arguments:
    name -- The name of the feed to save.
    stamp -- The timestamp to store with the RSS feed.
    """
    path = 'stamps/' + name + '.txt'
    with open(path, 'w') as f:
        f.write(str(stamp))

def load_timestamp_for_source(source):
    """
    Given a source (string), finds the last timestamp of when the source was
    last accessed
    """
    stamp = list(db.stamps.find({"source": source}))
    if stamp and len(stamp) == 1:
        return stamp[0]['timestamp']
    else:
        return None

def save_timestamp_for_source(source, stamp=datetime.utcnow()):
    if not stamp:
        stamp = datetime.utcnow()

    # Find a stamp with the given source and update the timestamp. Upsert
    # will do an insert if the source previously not in the db.
    db.stamps.update({'source': source},
        { 'timestamp': stamp, 'source': source },
        upsert=True)
