#This is an proof-of-concept for using the reddit API with userless client_credentials authentication to access the front page of the /r/jokes subreddit..

import requests
import requests.auth

appID = '' # Insert public App ID here
appSecret = '' # Insert App Secret here.
userAgent = "HGP Reddit Crawler"

get_token_address = "https://www.reddit.com/api/v1/access_token" # This is the url you must access to get an API token.

client_auth = requests.auth.HTTPBasicAuth(appID, appSecret) # Generates an object containing some of the information we need to authenticate.
post_data = {"grant_type": "client_credentials"} # We will be authenticating as a standalone application with no associated user.  This is the data the reddit API says we must include in the post data.
headers = {"User-Agent": userAgent} # For this authentication type, this is the header data we need.
response = requests.post(get_token_address, auth=client_auth, data=post_data, headers=headers)
accessToken = response.json()["access_token"] # The response from the server will contain many different items.  For this very simple proof-of-concept, we need only the access token.

authorization = "bearer "  # The api expects the access token to be formatted in a certain way
headers = {"Authorization": authorization, "User-Agent": userAgent}
response = requests.get("https://oauth.reddit.com/r/jokes", headers=headers) # Most endpoints in the API don't work for some reason; this one does

print str(response.json())
