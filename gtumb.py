import pytumblr
import yaml
from requests_oauthlib import OAuth1Session

request_token_url = 'http://www.tumblr.com/oauth/request_token'
authorize_url = 'http://www.tumblr.com/oauth/authorize'
access_token_url = 'http://www.tumblr.com/oauth/access_token'
YAML_PATH = '.tumblr'

stream = open(YAML_PATH, 'r')
keys = yaml.safe_load(stream)
stream.close()

# Step 1: Obtain request token
oauth_session = OAuth1Session(keys['consumer_key'], client_secret=keys['consumer_secret'])
fetch_response = oauth_session.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

# Step 2: Authorize URL + response
full_authorize_url = oauth_session.authorization_url(authorize_url)

# Redirect to authentication page
print('\nPlease go here and authorize:\n{}'.format(full_authorize_url))
redirect_response = input('Allow then paste the full redirect URL here:\n').strip()

# Retrieve oauth verifier
oauth_response = oauth_session.parse_authorization_response(redirect_response)
verifier = oauth_response.get('oauth_verifier')

# Step 3: Request final access token
oauth_session = OAuth1Session(
    keys['consumer_key'],
    client_secret=keys['consumer_secret'],
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier
)
oauth_tokens = oauth_session.fetch_access_token(access_token_url)

keys = {
    'consumer_key': keys['consumer_key'],
    'consumer_secret': keys['consumer_secret'],
    'oauth_token': oauth_tokens.get('oauth_token'),
    'oauth_token_secret': oauth_tokens.get('oauth_token_secret')
}

keydump = open(YAML_PATH, 'w+')
yaml.dump(keys, keydump, indent=2)
keydump.close()

client = pytumblr.TumblrRestClient(
    keys['consumer_key'],
    keys['consumer_secret'],
    keys['oauth_token'],
    keys['oauth_token_secret']
)
print(client.info())