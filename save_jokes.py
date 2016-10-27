from dbco import db
from pymongo.bulk import BulkOperationBuilder
from joke import Joke


def insertJokes(db, validJokes):
    for joke in validJokes:
        jokeJson = joke.create_json()
        db.jokes.update({'sourcleURL': joke.sourcleURL}, {'$set': jokeJson}, upsert=True)


def upsertJokes(jokes):
    if jokes:
        bulk = db.jokes.initialize_ordered_bulk_op()
        for joke in jokes:
            bulk.find({
                'sourceURL': joke.sourceURL
            }).upsert().update_one({
                '$set': joke.create_json()
            })

        result = bulk.execute()
        return result
    return None


def saveJokes(foundJokes):
    """Add valid jokes to the database."""

    jokes = filter(lambda joke: isinstance(joke, Joke), foundJokes)
    result = upsertJokes(jokes)
    return result
