
field_content = "content"
field_source = "source"
field_sourceURL = "sourceURL"
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

    def __init__(self, title, content, source, sourceURL, pubdate=None,
        entities=None, comments=None, upvotes=None, downvotes=None,
        timestamp=None, author=None, visited=False):

        # Necessary fields
        self.title = title
        self.content = content
        self.source = source  # ex: "reddit" or "jokerz"
        self.sourceURL = sourceURL

        # Optional Fields
        self.pubdate = pubdate

        self.entities = entities if entities else []
        self.comments = comments if comments else []
        self.upvotes = int(upvotes) if upvotes else 0
        self.downvotes = int(downvotes) if downvotes else 0

        # TODO: Migrate from pubdate to timestamp entirely.
        self.timestamp = timestamp if timestamp else pubdate

        self.author = author
        self.visited = bool(visited)

    def create_json(self):
        """
        Creates a JSON representation (a dict) of the joke.
        """
        document = {}
        document[field_content] = self.content
        document[field_source] = self.source
        document[field_sourceURL] = self.sourceURL
        document[field_pubdate] = self.pubdate
        document[field_title] = self.title
        document[field_entities] = self.entities
        document[field_comments] = self.comments
        document[field_upvotes] = self.upvotes
        document[field_downvotes] = self.downvotes
        document[field_timestamp] = self.timestamp
        document[field_author] = self.author
        document[field_visited] = self.visited

        return document

    def get_export_json(self):
        """
        Creates a JSON representation (a dict) of the joke that only has
        fields relevant to the webapp.
        """
        document = self.create_json()

        # Remove the fields webapp won't need
        document.pop(field_comments)
        document.pop(field_entities)
        document.pop(field_visited)

        # A temporary fix until we permanently change pubdate to timestamp in crawler
        document[field_timestamp] = document[field_pubdate]
        document.pop(field_pubdate)

        return document


    @classmethod
    def from_json(Joke, jokeJson):
        content = jokeJson.get(field_content)
        source = jokeJson.get(field_source)
        sourceURL = jokeJson.get(field_sourceURL)
        pubdate = jokeJson.get(field_pubdate)
        title = jokeJson.get(field_title)
        entities = jokeJson.get(field_entities)
        comments = jokeJson.get(field_comments)
        upvotes = jokeJson.get(field_upvotes)
        downvotes = jokeJson.get(field_downvotes)
        timestamp = jokeJson.get(field_timestamp)
        author = jokeJson.get(field_author)
        visited = jokeJson.get(field_visited)

        # Convert to appropriate data types as needed
        upvotes = int(upvotes) if upvotes else upvotes
        downvotes = int(downvotes) if downvotes else downvotes
        timestamp = long(timestamp) if timestamp else timestamp
        visited = bool(visited)

        return Joke(title, content, source, sourceURL, pubdate=pubdate,
        entities=entities, comments=comments, upvotes=upvotes,
        downvotes=downvotes, timestamp=timestamp, author=author, visited=visited)


    def is_valid(self):
        """
        Returns true if title, content, source, sourceURL are all
        non-empty strings
        """
        return all([self.title, self.content, self.source, self.sourceURL])


    def __repr__(self):
        template = "Joke Title: {}\tVisited: {}"
        title, visited = self.title, self.visited
        return template.format(title.encode('ascii', 'ignore'), visited)


    def __str__(self):
        template = "Joke Title: {}\tVisited: {}"
        title, visited = self.title, self.visited
        return template.format(title.encode('ascii', 'ignore'), visited)
