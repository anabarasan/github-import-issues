from config import SOURCE_REPO, TARGET_REPO
import issues, labels, milestones, comments
from common import request, done

request(SOURCE_REPO, "labels")

src_repo_labels = labels.read(SOURCE_REPO)
tgt_repo_labels = labels.read(TARGET_REPO)
     
# delete the labels in target repo
for key in tgt_repo_labels.keys():
    labels.delete(TARGET_REPO, key)
         
# create the lables in target repo
for key in src_repo_labels.keys():
    labels.create(TARGET_REPO, key, src_repo_labels[key][key])
    #print key, tgt_repo_labels[key][key]
     
###################################################
   
src_milestones = milestones.read(SOURCE_REPO)
    
# create the milestones in target
milestone_map={}
for key in src_milestones.keys():
    new_milestone_no = milestones.create(TARGET_REPO, key, src_milestones[key][key][0])
    milestone_map[src_milestones[key][key][1]] = new_milestone_no
#     print TARGET_REPO, key, src_milestones[key][key][0]
print milestone_map
###################################################

# create the issues in target
def create_issues(issue_list, milestone_no_map, status="open"):
    i = 0
    limit = len(issue_list)
     
    while i < limit:
        issue = issue_list[i]
        
        no_of_comments = issue['comments']
        issue_id = issue['id']
        del issue['comments']
        del issue['id']
        
        if issue.has_key('milestone'):
            issue['milestone'] = milestone_no_map[issue['milestone']]
    
        new_issue_id = issues.create(TARGET_REPO, issue)
        
        # does the issue have comments? if so create them.
        if no_of_comments > 0:
            comments_list = sorted(comments.read(SOURCE_REPO, issue_id), key=lambda k: k['id'])
            
            j = 0
            
            while j < no_of_comments:
                comment= comments_list[j]["comment"]
                comments.create(TARGET_REPO, new_issue_id, comment) 
                j+=1
                
        if status == "closed":
            modified_issue = {"state":"closed"}
            issues.edit(TARGET_REPO, new_issue_id, modified_issue)
            
        i+=1
    
print "########################################## \ncreating open issues"
src_repo_open_issue_list = issues.read(SOURCE_REPO)
create_issues(src_repo_open_issue_list, milestone_map)
print "########################################## \ncreating closed issues"
src_repo_closed_issue_list = issues.read(SOURCE_REPO,"closed")
create_issues(src_repo_closed_issue_list, milestone_map, "closed")

done();
 
###################################################
    
# test code
# labels.create(SOURCE_REPO, "CreatedWithAPI", "000000")
# labels.delete(SOURCE_REPO, "CreatedWithAPI")
# print milestones.create(SOURCE_REPO, "TestMilestone", None)
# TestIssue = {"title":"title1", "body":"body", "assignee":"anabarasan"}
# issues.create(SOURCE_REPO, TestIssue)