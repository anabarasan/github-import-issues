import base64, json, urllib2
from config import GITHUB_USERNAME, GITHUB_PASSWORD

BASEURL = "https://api.github.com"

def request(api, method=None, data=None):
    request = urllib2.Request(BASEURL + api)
    authstring = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % authstring)
    request.add_header("User-Agent",GITHUB_USERNAME)
    if (method is not None):
        request.get_method = lambda: method
    try:
        if (data is not None):
            data = json.dumps(data)
            return urllib2.urlopen(request, data)
        else:
            return urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print e.read()
        import sys
        sys.exit(0)
    
def getLimits():
    response = request("/rate_limit")
    print "################################################"
    print "X-RateLimit-Limit     ", response.info().getheader("X-RateLimit-Limit")
    print "X-RateLimit-Remaining ", response.info().getheader("X-RateLimit-Remaining")
    print "X-RateLimit-Reset     ", response.info().getheader("X-RateLimit-Reset")
    print "################################################"

def done():
    print "######################################"
    print "\t\t\t\t DONE"
    print "######################################"
    
