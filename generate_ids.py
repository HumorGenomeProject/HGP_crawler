from dbco import db


def create_jokeId():
    '''
    Returns a unique jokeId. Increments count in counter collection
    '''
    count = db.counters.find_and_modify(
        query={
            '_id': 'jokeId',
        },
        update={
            '$inc': { 'value': 7 },  # update by a constant prime number
        }
    )

    result = count.get('value')
    if result:
        return int(result)
    else:
        return None

def create_userId():
    '''
    Returns a unique jokeId. Increments count in counter collection
    '''
    count = db.counters.find_and_modify(
        query={
            '_id': 'userId',
        },
        update={
            '$inc': { 'value': 7 },  # update by a constant prime number
        }
    )

    result = count.get('value')
    if result:
        return int(result)
    else:
        return None
