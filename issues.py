from config import GITHUB_USERNAME, GITHUB_PASSWORD
import base64, json, urllib2

def read(repository, state="open"):
    # GET /repos/:owner/:repo/issues
    request = urllib2.Request("https://api.github.com/repos/%s/issues?state=%s" % (repository, state))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)  
    response = urllib2.urlopen(request)

    result = response.read()
    
    issues = json.loads(result)
    
    i = 0
    limit = len(issues)
    
    issue_list = []
    
    while i < limit:
        
        issue_dict = {}
        
        issue_dict["title"] = issues[i]["title"]
        if issues[i]["body"] != None:
            issue_dict["body"] = issues[i]["body"]
        if issues[i]["assignee"] != None:
            issue_dict["assignee"] = issues[i]["assignee"]["login"]
        if issues[i]["milestone"] != None:
            issue_dict["milestone"] = int(issues[i]["milestone"]["number"])
        label_list = issues[i]["labels"]
        
        labels = []
        
        j = 0
        maxlabels = len(label_list)
        
        while j < maxlabels:
            labels.append(label_list[j]["name"])
            j+=1
        
        issue_dict["labels"] = labels
        issue_dict["comments"] = issues[i]["comments"]
        issue_dict["id"] = issues[i]["number"]
            
        issue_list.append(issue_dict)        
        
        i+=1 
        
    return issue_list

def create(repository, issue):
    # POST /repos/:owner/:repo/issues
    request = urllib2.Request("https://api.github.com/repos/%s/issues" % (repository))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    request.get_method = lambda: "POST"
    data = json.dumps(issue)
    response = urllib2.urlopen(request, data)
    new_issue = json.loads(response.read())
    print "Create issue ", new_issue["number"], " response : ", new_issue
    return new_issue["number"]

def edit(repository, issue_id, issue):
    # PATCH /repos/:owner/:repo/issues/:number
    request = urllib2.Request("https://api.github.com/repos/%s/issues/%s" % (repository, issue_id))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    request.get_method = lambda: "PATCH"
    data = json.dumps(issue)
    response = urllib2.urlopen(request, data)
    new_issue = json.loads(response.read())
    print "Editing issue ", new_issue["number"], " response : ", new_issue