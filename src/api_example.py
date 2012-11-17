import web, json
from web_utils import *

# necessary definitions for OAuth and REST API login

# our Bullhorn OAuth client ID
client_id = 'b3892ddc-8b3a-4f8e-8aba-17df88d35b3a'
# our Bullhorn OAuth secret
client_secret = 'bhPartner33'
# Bullhorn OAuth service endpoint
oauth_base_url = 'https://auth9.bullhornstaffing.com/oauth'
# Bullhorn REST API service endpoint
api_base_url = 'https://rest9.bullhornstaffing.com/rest-services'


urls = (
	'/bhczc', 'index',
	'/bhczc/reset', 'reset',
    '/bhczc/userid', 'userid'
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
        return json_http_call("%s/%s?%s" % (session.rest_url, command, join_dict(params)))
    else:
        return json_http_call("%s/%s" % (session.rest_url, command), join_dict(params))

class index:
    def GET(self):
        if session.access_token is None:
            params = parseQuery(web.ctx.query)
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

        data = api_call("settings/userId")["userId"]
        
        return "state=%s<br>data=" % (params.state, str(data))

class userid:
    def GET(self):
        if session.rest_token is None:
            raise web.seeother(oauth_base_url + "/authorize?client_id=%s&response_type=code&redirect_uri=%s"
                % (client_id, "http://172.27.1.131:9099/bhczc/"))

        return "foo"

class reset:
	def GET(self):
		session.kill()
		return "session reset"

if __name__ == "__main__":
	app.run()
