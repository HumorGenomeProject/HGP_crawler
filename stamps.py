from dbco import db
from datetime import datetime

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
