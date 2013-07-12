from common import request

def read(repository):
    # GET /repos/:owner/:repo/milestones
    response = request("/repos/%s/milestones" % (repository))
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
    data = {"title":name}
    if (duedate != None):
        data["due_on"] = duedate
    response = request("/repos/%s/milestones" % (repository), "POST", data)
    response_info = response.read()
    print "Creating milestone ", name, " response : ", response_info
#    response_info = json.loads(response_info)
#    return response_info['number']
