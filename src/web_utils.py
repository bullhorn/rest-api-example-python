import urllib2, json

def parseQuery(q):
	after_qmark = q[1:]
	if (len(after_qmark) < 2):
		return { }
	return dict([p.split("=") for p in q[1:].split("&")])

def build_querystring(d):
    return '&'.join(['%s=%s' % (str(k), str(v)) for k, v in d.items()]) 

def json_http_call(url, data=None):
    try:
        if data is None:
            res = urllib2.urlopen(url)
        else:
            res = urllib2.urlopen(url, data)
        data = res.read() 
    except urllib2.HTTPError, e:
        data = e.read()
        print "error in request: " + url + ": " + data

    return json.loads(data)

