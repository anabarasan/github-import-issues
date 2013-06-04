from config import GITHUB_USERNAME, GITHUB_PASSWORD
import base64, json, urllib2

def read(repository):
    # GET /repos/:owner/:repo/labels
    request = urllib2.Request("https://api.github.com/repos/%s/labels" % (repository))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)  
    response = urllib2.urlopen(request)
    
    result = response.read()
    
    labels = json.loads(result)
    
    i = 0
    limit = len(labels)
    
    labels_dict = {}
    
    while i < limit:
        label_dict = {}
        label_name = labels[i]['name']
        label_color = labels[i]['color']
        label_dict[label_name] = label_color
        
        labels_dict[label_name] = label_dict 
        
        i+=1 
        
    return labels_dict

def delete(repository, name):
    # DELETE /repos/:owner/:repo/labels/:name
    request = urllib2.Request("https://api.github.com/repos/%s/labels/%s" % (repository, name))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    request.get_method = lambda: "DELETE"  
    response = urllib2.urlopen(request)
    print "delete ", name, " response : ", response.read()
    
def create(repository, name, color):
    
    request = urllib2.Request("https://api.github.com/repos/%s/labels" % (repository))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    data = {"name":name, "color":color}
    data = json.dumps(data)
    response = urllib2.urlopen(request, data)
    print "Create label ", name, " response : ", response.read()