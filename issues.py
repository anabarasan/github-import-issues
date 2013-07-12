from common import request

def read(repository, state="open"):
    # GET /repos/:owner/:repo/issues
    response = request("/repos/%s/issues?state=%s" % (repository, state))
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
    response = request("/repos/%s/issues" % (repository), "POST", issue)
    new_issue = json.loads(response.read())
    print "Creating issue #", new_issue["number"], " response : ", new_issue
    return new_issue["number"]

def edit(repository, issue_id, issue):
    # PATCH /repos/:owner/:repo/issues/:number
    response = request("/repos/%s/issues/%s" % (repository, issue_id), "PATCH", issue)
    new_issue = json.loads(response.read())
    print "Editing issue #", new_issue["number"], " response : ", new_issue
