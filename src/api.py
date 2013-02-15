from web_utils import *

base_url = 'https://rest.bullhornstaffing.com/rest-services'
rest_token_param = "BhRestToken"
rest_url_param = "restUrl"

class ApiLogin:
	def __init__(self, rest_url, rest_token):
		self.rest_url = rest_url 
		self.rest_token = rest_token 

def login(access_code):
    """
    Logs in to the REST API given an OAuth access token.  Returns a dictionary
    containing the data returned by the login call.  This includes:
       - The API endpoint URL
       - An authentication token
    Subsequent calls to the API must use the endpoint URL as their base URL,
    and must send the authentication token as a request parameter called 'BhRestToken'
    """
    login_data = json_http_call(base_url + '/login?version=*&access_token=' + access_code)
    return ApiLogin(login_data[rest_url_param], login_data[rest_token_param])

def make_call(endpoint, token, command, method='GET', params=None):
    if params is None:
        params = { }
    params[rest_token_param] = token

    http_params = build_querystring(params)

    if method == 'GET':
        return json_http_call("%s%s?%s" % (endpoint, command, http_params))
    else:
        return json_http_call("%s%s" % (endpoint, command), http_params)
