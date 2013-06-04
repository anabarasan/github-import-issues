import base64
import urllib2

from config import GITHUB_USERNAME, GITHUB_PASSWORD, DEBUG

def request(repository, api):
    
    request = urllib2.Request("https://api.github.com/repos/%s/%s" % (repository, api))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)  
    response = urllib2.urlopen(request)
    
    if(DEBUG):
        print "X-RateLimit-Limit", response.info().getheader("X-RateLimit-Limit")
        print "X-RateLimit-Remaining", response.info().getheader("X-RateLimit-Remaining")
        print "######################################"
    return response

def done():
    print "######################################"
    print "\t\t\t\t DONE"
    print "######################################"
    