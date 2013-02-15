import web, json, urllib
import oauth, api
from web_utils import *

app_base_path = '/sample'
oauth_redirect_path = app_base_path + '/oauth-callback'

urls = (
    app_base_path, 'userid',
	oauth_redirect_path, 'auth',
	app_base_path + '/logout', 'reset'
)

"""
Set up a web.py application with session data stored on disk.
"""
app = web.application(urls, globals())
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),
        initializer={'count': 0, 'access_token': None, 'rest_token': None, 'rest_url': None})
    web.config._session = session
else:
    session = web.config._session


def oauth_redirect_uri():
    return web.ctx.home + oauth_redirect_path

def auth_check():
    if session.rest_token is None:
        raise web.seeother(oauth.build_authorize_url(web.ctx.path, oauth_redirect_uri()))

def api_call(command, method='GET', params=None):
    return api.make_call(session.rest_url, session.rest_token, command, method, params)


class auth:
    """
    The OAuth authentication callback.  This will negotiate
    an access token with Bullhorn OAuth given an authorization
    token on the query string.  It will then use that access
    token to obtain a REST API token.

    The redirect URIs communicated to Bullhorn in your OAuth
    configuration must contain the URI to this request handler.

    Once the user enters credentials on the Bullhorn OAuth 
    login page, his/her browser will be redirected here, with
    a "code" query parameter appended, containing an authorization
    code.
    """
    def GET(self):
        # parse the query string into a dictionary
        params = parseQuery(web.ctx.query)
        if session.access_token is None:
            if 'code' in params:
                session.access_token = oauth.get_access_token(params['code'], oauth_redirect_uri())
            else:
                web.ctx.status = "400"
                return "oauth authorization code missing from parameters"

        api_login_data = api.login(session.access_token)
        session.rest_url = api_login_data.rest_url
        session.rest_token = api_login_data.rest_token

        if 'state' in params:
            redirect = urllib.unquote(params['state'])
        else:
            redirect = app_base_path
        raise web.seeother(redirect)

class userid:
    """
    Our sample API call.  Simply gets the logged-in user's
    user ID using the /settings call.
    """
    def GET(self):
        auth_check()
        data = api_call("settings/userId")
        return "your user ID is: %s" % data["userId"] 

class reset:
    """
    Clears the session.
    """
    def GET(self):
        session.kill()
        return "session reset"

if __name__ == "__main__":
    app.run()
