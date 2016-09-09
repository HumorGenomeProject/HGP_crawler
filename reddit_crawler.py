import requests
import requests.auth
import json
from joke import Joke
import stamps
import hgp_jokes
from datetime import datetime, timedelta

secretsfile = "secrets.json"
user_agent = "Humor Genome Project Reddit Crawler"

def create_token(app_id, app_secret):
	"""
	Produces an OAUTH token using an app_id as a username and a app_secret as a password.
	"""
	# Must make a POST here to get a OAUTH token
	url = "https://www.reddit.com/api/v1/access_token"
	basic_auth = requests.auth.HTTPBasicAuth(app_id, app_secret)

	post_body = {"grant_type": "client_credentials"}
	headers = {"User-Agent": user_agent}
	response = requests.post(url, auth=basic_auth, data=post_body, headers=headers)

	if response.status_code == 200:
		token = response.json()["access_token"]
		return token
	
	else:
		return None


def get_posts_from_subreddit(token, subreddit, last_timestamp=None):
	"""
	Takes a subreddit in the form of a string and fetches all
	jokes from this subreddit page that were posted past
	the given timestamp.

	Returns: a list of Jokes.

	subreddit must be a string, last_timestamp must be a 
	"""
	authorization = "bearer " +  token
	headers = {"Authorization": authorization, "User-Agent": user_agent}

	jokes = []
	sub_pages = ['new', 'rising', 'hot']

	for sub_page in sub_pages:

		url = "https://oauth.reddit.com/r/{}/new".format(subreddit)

		response = requests.get(url, headers=headers) # Most endpoints in the API don't work for some reason; this one does
		results = response.json()

		if 'data' not in results:
			return None

		data = results['data']

		if 'children' not in data:
			return None

		posts = data['children']

		for post in posts:
			actual_post = post['data']
			upvotes = actual_post['ups']
			downvotes = actual_post['downs']
			title = actual_post['title']
			content = actual_post['selftext']
			sourceUrl = actual_post['url']
			pubdate = datetime.fromtimestamp(int(actual_post['created']))

			guid = sourceUrl

			if not last_timestamp or pubdate >= last_timestamp:
				# These jokes are new compared to the last times we checked. Keep them
				aJoke = Joke(content, 'reddit', sourceUrl, guid, pubdate=pubdate, title=title, upvotes=upvotes, downvotes=downvotes)
				jokes.append(aJoke)

	return jokes


def main():
	with open(secretsfile) as sf:
		secrets = json.load(sf)

	if "reddit_api" not in secrets:
		raise ValueError("Could not find reddit credentials.")
	
	reddit_api = secrets.get("reddit_api")

	if 'app_id' not in reddit_api or 'app_secret' not in reddit_api:
		raise ValueError("Could not find reddit credentials.")		

	app_id = reddit_api["app_id"]
	app_secret = reddit_api["app_secret"]

	token = create_token(app_id, app_secret)

	if token is None:
		raise ValueError("Failed to create a token for the reddit API")


	subreddits = ['jokes', 'humor', 'funny']
	for subreddit in subreddits:
		source = "reddit" + "." + subreddit
		last_timestamp = stamps.load_timestamp_for_source(source)
		jokes = get_posts_from_subreddit(token, subreddit, last_timestamp)
		
		# Update the timestamps collection
		current_time = datetime.utcnow()
		# Timestamps by reddit are 4 hours ahead
		adjusted_timestamp = current_time + timedelta(hours=4)
		stamps.save_timestamp_for_source(source, stamp=adjusted_timestamp)

		# Save the jokes
		if jokes:
			result = hgp_jokes.saveJokes(jokes)
			if result:
				# Print how many modified and how many updated
				local_time = datetime.now()
				print "Subreddit: /r/{}\tCreated: {}\tModified: {}\tTimestamp: {}".format(subreddit,
					result['nUpserted'], result['nModified'], local_time)


if __name__ == '__main__':
	main()
