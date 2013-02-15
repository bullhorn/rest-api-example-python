from web_utils import *

# Bullhorn OAuth client ID
client_id = "CLIENT_ID_HERE"

# Bullhorn OAuth secret
client_secret = 'CLIENT_SECRET_HERE'

# Bullhorn OAuth service endpoint
base_url = 'https://auth.bullhornstaffing.com/oauth'

def get_access_token(code, redirect_url):
    """
    Gets an OAuth access token given an OAuth authorization code
    """
    access_token_params = build_querystring({
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_url,
        'code': code
    })
    
    access_token_response = json_http_call(base_url + '/token', access_token_params)
    print("=====> " + str(access_token_response))
    return access_token_response["access_token"]

def build_authorize_url(state, redirect_url):
    qstr = build_querystring({
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_url,
        "state": state
    })

    return base_url + "/authorize?" + qstr
