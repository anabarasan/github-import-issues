from config import GITHUB_USERNAME, GITHUB_PASSWORD
import base64, json, urllib2

def read(repository, issue_id):
    # GET /repos/:owner/:repo/issues/:number/comments
    request = urllib2.Request("https://api.github.com/repos/%s/issues/%s/comments" % (repository,issue_id))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)  
    response = urllib2.urlopen(request)

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
    request = urllib2.Request("https://api.github.com/repos/%s/issues/%s/comments" % (repository,issue_id))
    base64string = base64.encodestring('%s:%s' % (GITHUB_USERNAME, GITHUB_PASSWORD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    request.get_method = lambda: "POST" 
    data = {'body':comment} 
    data = json.dumps(data)
    try:
        response = urllib2.urlopen(request, data)
    except urllib2.HTTPError, e:
        print e.read()
        import sys
        sys.exit(0)
    print "Create comment for issue #", issue_id, " response : ", response.read()
