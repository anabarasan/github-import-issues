from config import GITHUB_USERNAME, GITHUB_PASSWORD
import base64, json, urllib2

def read(repository):
    # GET /repos/:owner/:repo/milestones
    request = urllib2.Request("https://api.github.com/repos/%s/milestones" % (repository))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)  
    response = urllib2.urlopen(request)
    
    result = response.read()

    milestones = json.loads(result)
    
    i = 0
    limit = len(milestones)
    
    milestones_dict = {}
    
    while i < limit:
        milestone_dict = {}
        
        title = milestones[i]['title']
        due_on = milestones[i]['due_on']
        number = milestones[i]['number']
        milestone_dict[title] = [due_on, number]
         
        milestones_dict[title] = milestone_dict 
        
        i+=1 
        
    return milestones_dict

def create(repository, name, duedate=None):
    # POST /repos/:owner/:repo/milestones
    request = urllib2.Request("https://api.github.com/repos/%s/milestones" % (repository))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    request.get_method = lambda: "POST"
    
    data = {"title":name}
    if (duedate != None):
        data["due_on"] = duedate
    
    data = json.dumps(data)
    
    try:
        response = urllib2.urlopen(request, data)
    except urllib2.HTTPError, e:
        print e.read()
        import sys
        sys.exit(0)
    
    response_info = response.read()
    print "Create milestone ", name, " response : ", response_info
    response_info = json.loads(response_info)
    return response_info['number']