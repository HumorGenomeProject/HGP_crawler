from dbco import db, webapp_db
from joke import Joke, field_sourceURL
import generate_ids
from copy import deepcopy
import generate_ids

field_exported = 'exported_to_webapp'
field_visited = 'visited'

def jokes_to_export(limit=1000):
    '''
    Find jokes that need to be exported from the crawler DB
    and exported to the webapp db
    '''
    jokes = db.jokes.find(
        {
            # Only export jokes that have had content crawled
            field_visited: True,
            field_exported: {
                # Never exported to webapp
                '$in': [None, False]
            }
        }).limit(limit)

    return list(jokes)


def update_crawler(joke, crawler_bulk):
    '''
    Updates crawler db to mark this joke as exported
    '''
    joke[field_exported] = True

    crawler_bulk.find({
        field_sourceURL: joke[field_sourceURL]
    }).upsert().update_one({
        # Update with the new joke, which now has an exported field
        '$set': joke
    })

def export_webapp(joke, webapp_bulk):
    '''
    Exports a joke into the webapp database. Adds a jokeId field
    '''

    jokeId = generate_ids.create_jokeId()
    joke['jokeId'] = jokeId

    webapp_bulk.find({
        field_sourceURL: joke[field_sourceURL]
    }).upsert().update_one({
        '$set': joke
    })


def main():
    """
    This script exports jokes from the hgp_crawler database to the hgp_webapp
    database.
    """
    jokes = jokes_to_export(limit=100)
    if jokes:
        crawler_bulk = db.jokes.initialize_ordered_bulk_op()
        webapp_bulk = webapp_db.jokes.initialize_ordered_bulk_op()

        for joke in jokes:
            update_crawler(joke, crawler_bulk)
            # Convert to a python Joke object
            joke_obj = Joke.from_json(joke)
            # Then, store it in webapp as json w/ only the fields relevant
            # to webapp
            export_webapp(joke_obj.get_export_json(), webapp_bulk)

        # Only execute if any unexported jokes to execute on
        crawler_result = crawler_bulk.execute()
        print "Crawler result: \n{}".format(crawler_result)
        webapp_result = webapp_bulk.execute()
        print "\nWebapp result: \n{}".format(webapp_result)

    else:
        print "No unexported jokes found"

if __name__ == '__main__':
    main()
