import web, json
from web_utils import *

# necessary definitions for OAuth and REST API login
# our Bullhorn OAuth client ID
#client_id = '06ab09e7-b391-4e1c-a399-f3eca4475a81'
#client_id = '6717406-d8b5-494c-8366-fc483b67a6b5'
#client_id = '07d763a1-abfa-4ac5-840e-cee9157ab539'
client_id = '42b64d2e-457e-4b9d-a6ab-4e9ebfeb2e7f'
#client_id = 'b3892ddc-8b3a-4f8e-8aba-17df88d35b3a'
# our Bullhorn OAuth secret
client_secret = 'bhsecret'
# Bullhorn OAuth service endpoint
oauth_base_url = 'http://172.27.1.131:9292/oauth-services'
oauth_redirect_url = 'http://localhost:9099/sample/oauth-callback'
# Bullhorn REST API service endpoint
api_base_url = 'http://ws:9090/rest-services'


urls = (
	'/sample/oauth-callback', 'auth',
	'/sample/logout', 'reset',
    '/sample/userid', 'userid'
)

app = web.application(urls, globals())
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),
        initializer={'count': 0, 'access_token': None, 'rest_token': None, 'rest_url': None})
    web.config._session = session
else:
    session = web.config._session

def oauth_login(code):
    noencode_params = join_dict({
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': oauth_redirect_url,
        'code': code
    })
    
    return json_http_call(oauth_base_url + '/token', noencode_params)

def api_login(access_code):
    return json_http_call(api_base_url + '/login?version=*&access_token=' + access_code, None)

def api_call(command, method='GET', params=None):
    if params is None:
        params = { }
    params["BhRestToken"] = session.rest_token

    if method == 'GET':
        return json_http_call("%s%s?%s" % (session.rest_url, command, join_dict(params)))
    else:
        return json_http_call("%s%s" % (session.rest_url, command), join_dict(params))

def auth_check(sess, path):
    if session.rest_token is None:
        qstr = join_dict({
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": oauth_redirect_url,
            "state": path
        })

        raise web.seeother(oauth_base_url + "/authorize?" + qstr)

class auth:
    def GET(self):
        params = parseQuery(web.ctx.query)
        if session.access_token is None:
            if "code" in params:
                auth_token = params['code']
                oauth_data = oauth_login(auth_token)
                print(str(oauth_data))
                session.access_token = oauth_data["access_token"]
            else:
                raise web.seeother(oauth_base_url + "/authorize?client_id=%s&response_type=code" % (client_id))

        if session.rest_token is None:
            api_login_data = api_login(session.access_token)
            session.rest_token = api_login_data["BhRestToken"]
            session.rest_url = api_login_data["restUrl"]
        print(params["state"])    
        raise web.seeother(params['state'])

class userid:
    def GET(self):
        auth_check(session, web.ctx.path) #web.ctx.homepath)
        data = api_call("settings/userId")
        print(web.ctx.path)
        return "your user ID is: %s" % data["userId"]

class reset:
	def GET(self):
		session.kill()
		return "session reset"

if __name__ == "__main__":
	app.run()
