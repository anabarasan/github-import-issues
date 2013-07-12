from common import request

def read(repository):
    # GET /repos/:owner/:repo/labels
    response = request("/repos/%s/labels" % (repository))
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
    response = request("/repos/%s/labels/%s" % (repository, name), "DELETE")
    print "delete ", name, " response : ", response.read()
    
def create(repository, name, color):
    # POST /repos/:owner/:repo/labels
    data = {"name":name, "color":color}
    response = request("/repos/%s/labels" % (repository), "POST", data)
    print "Create label ", name, " response : ", response.read()
