# python script
# Imports
import sys
import webbrowser
import requests
import subprocess
import shlex
import re
import json
from BeautifulSoup import BeautifulSoup

def write(json):
	try:
		file = open(issueID,'a')  
		file.write(json)
		file.close()

	except:
		sys.exit(0) 

#variables
files = []
arrayPrevCommits= []
data = {}
issueID = sys.argv[1]
data['issueID']= issueID
urlIssueGithub = "https://github.com/elastic/elasticsearch/issues/"+issueID
webbrowser.open_new_tab(urlIssueGithub)

fixedID = raw_input("Please enter the FIX issue ID %s: " %issueID)
data['fixedID']= fixedID
if fixedID != "NONE":
	urlFixedID='https://github.com/elastic/elasticsearch/pull/'+fixedID
	webbrowser.open_new_tab(urlFixedID)

commit = raw_input("Please enter the commit ID :" )
data['commitID']= commit
urlCommit='https://github.com/elastic/elasticsearch/commit/'+commit
webbrowser.open_new_tab(urlCommit)
response=requests.get(urlCommit)
html = response.content
soup = BeautifulSoup(html)

for span in soup.findAll('span'):
	if 'parents' in span.text:
		string = span.text
		parents = string.split('parents')
		parent = parents[-1].split('+')
		parentID = parent[0]
		print parentID
	elif 'parent' in span.text:
		string = span.text
		parents = string.split('parent')
		parentID = parents[-1]
data['parentID']= parentID

for link in soup.findAll('a', href=True):
	if ('diff-' in link['href']):
		if link.text != "":
			match = re.search(r'/test/', link.text)
			if not match:
				files.append(link.text)		
data['files']= files

for i in files:
 	command_line = "sh elastic.sh "+parentID+" "+i
 	args = shlex.split(command_line)
 	p = subprocess.Popen(args)
	
 	previousCommits = raw_input("Please enter the possible previous commits in %s: " %i)
 	arrayPrevCommits.append(previousCommits+'@'+i)
 	while previousCommits !="":     
 		previousCommits = raw_input("Please enter the possible previous commits in %s: " %i)
 		if previousCommits !="":
 			arrayPrevCommits.append(previousCommits+'@'+i)
data['previousCommit']= arrayPrevCommits

for prev in arrayPrevCommits:
 	commit_file = prev.split('@')
 	if commit_file[0]!="": 
 		command_line = "cd elasticsearch; git log "+commit_file[0]+"^ --oneline | sed -n 1,1p"
		output = subprocess.check_output(command_line, shell=True)
	
		parentOfParent = output.split(' ')
	 	webbrowser.open_new_tab('https://github.com/elastic/elasticsearch/blame/'+parentOfParent[0]+'/'+commit_file[-1])

json_data = json.dumps(data)
write(json_data)
