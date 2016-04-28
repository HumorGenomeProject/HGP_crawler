from collections import namedtuple
import json
from dbco import * # this imports the db connection
from datetime import datetime

field_content = "content"
field_source = "source"
field_sourceURL = "sourceURL"
field_guid = "guid"
field_title = "title"
field_entities = "entities"
field_comments = "comments"
field_upvotes = "upvotes"
field_downvotes = "downvotes"
field_upvotes = "upvotes"
field_timestamp = "timestamp"
field_pubdate = "pubdate"
field_author = "author"
field_visited = "visited"

class Joke(object):

    def __init__(self, content, source, sourceURL, guid, pubdate=None, title=None, entities=None, comments=None, upvotes=None, downvotes=None, timestamp=None, author=None, visited=False):
        self.content = content
        self.source = source
        self.sourceURL = sourceURL
        self.guid = guid
        self.pubdate = pubdate
        self.title = title
        self.entities = entities
        self.comments = comments
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.timestamp = timestamp
        self.author = author
        self.visited = visited

    def createJson(self):
        document = {}
        document[field_content] = self.content
        document[field_source] = self.source
        document[field_sourceURL] = self.sourceURL
        document[field_pubdate] = self.pubdate
        document[field_guid] = self.guid
        document[field_title] = self.title
        document[field_entities] = self.entities
        document[field_comments] = self.comments
        document[field_upvotes] = self.upvotes
        document[field_downvotes] = self.downvotes
        document[field_timestamp] = self.timestamp
        document[field_author] = self.author

        document = {key: val for key, val in document.iteritems() if val}

        # Always add in after so visited field always shows in JSON
        document[field_visited] = self.visited

        return document

    @classmethod
    def fromJson(Joke, jokeJson):
        content = jokeJson.get(field_content)
        source = jokeJson.get(field_source)
        sourceURL = jokeJson.get(field_sourceURL)
        pubdate = jokeJson.get(field_pubdate)
        guid = jokeJson.get(field_guid)
        title = jokeJson.get(field_title)
        entities = jokeJson.get(field_entities)
        comments = jokeJson.get(field_comments)
        upvotes = jokeJson.get(field_upvotes)
        downvotes = jokeJson.get(field_downvotes)
        timestamp = jokeJson.get(field_timestamp)
        author = jokeJson.get(field_author)
        visited = jokeJson.get(field_visited)

        if visited is None:
            visited = False

        # Convert to appropriate data types as needed
        upvotes = int(upvotes) if upvotes else upvotes
        downvotes = int(downvotes) if downvotes else downvotes
        timestamp = long(timestamp) if timestamp else timestamp

        return Joke(content, source, sourceURL, guid, pubdate, title, entities, comments, upvotes, downvotes, timestamp, author, visited)


    def isValid(self):
        '''Returns true if content, source, sourceURL are all actual values and non-empty strings'''
        return all([self.content, self.source, self.sourceURL])

    def __repr__(self):
        template = "Joke Title: {}\tVisited: {}"
        title, visited = self.title, self.visited
        if not title:
            title = ''
        return template.format(title.encode('ascii', 'ignore'), visited)

    def __str__(self):
        template = "Joke Title: {}\tVisited: {}"
        title, visited = self.title, self.visited
        if not title:
            title = ''
        return template.format(title.encode('ascii', 'ignore'), visited)
