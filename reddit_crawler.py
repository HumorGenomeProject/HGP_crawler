import requests
import requests.auth
import json
from joke import Joke

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
	url = "https://oauth.reddit.com/r/{}/new".format(subreddit)

	response = requests.get(url, headers=headers) # Most endpoints in the API don't work for some reason; this one does
	results = response.json()

	if 'data' not in results:
		return None

	data = results['data']

	if 'children' not in data:
		return None

	posts = data['children']

	jokes = []
	for post in posts:
		actual_post = post['data']
		upvotes = actual_post['ups']
		downvotes = actual_post['downs']
		title = actual_post['title']
		content = actual_post['selftext']
		sourceUrl = actual_post['url']
		pubdate = int(actual_post['created'])

		guid = sourceUrl

		if pubdate >= last_timestamp:
			# Create and store the joke only if it is newer than the last timestamp
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

	jokes = get_posts_from_subreddit(token, "jokes")
	print jokes


	# TODO
	# For now we are just printing the jokes. Must use timestamps and the db
	# to track which jokes we've already seen

	# Also, must revisit these permalinks since most jokes are brand-new. Want
	# updated upvote/downvote/comments for each


if __name__ == '__main__':
	main()
