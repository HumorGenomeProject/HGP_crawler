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
            '$inc': { 'value': 7 },
        }
    )

    result = count.get('value')
    if result:
        return int(result)
    else:
        return 0

def create_userId():
    '''
    Returns a unique jokeId. Increments count in counter collection
    '''
    count = db.counters.find_and_modify(
        query={
            '_id': 'userId',
        },
        update={
            '$inc': { 'value': 7 },
        }
    )

    result = count.get('value')
    if result:
        return int(result)
    else:
        return 0


def test():
    val = create_jokeId()
    print "jokeId: {}".format(val)
    val = create_userId()
    print "userId: {}".format(val)


if __name__ == '__main__':
    test()
