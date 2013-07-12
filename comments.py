from common import request

def read(repository, issue_id):
    # GET /repos/:owner/:repo/issues/:number/comments
    response = request("/repos/%s/issues/%s/comments" % (repository,issue_id))
    result = response.read()
    comments = json.loads(result)
    i = 0
    limit = len(comments)
    comment_list = []
    while i < limit:
        comment_dict = {}
        comment_dict["id"] = int(comments[i]["id"])
        comment_dict["comment"] = "@%s commented on %s\n%s" % (comments[i]["user"]["login"], comments[i]["created_at"], comments[i]["body"])
        comment_list.append(comment_dict)
        i+=1
    return comment_list

def create(repository, issue_id, comment):
    # POST /repos/:owner/:repo/issues/:number/comments
    response = request("/repos/%s/issues/%s/comments" % (repository,issue_id), "POST", data)
    print "Creating comment for issue #", issue_id, " response : ", response.read()
