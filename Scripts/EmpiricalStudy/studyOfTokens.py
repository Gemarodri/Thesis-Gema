# python script
# Imports
import sys
import webbrowser
import subprocess
import shlex
import json

fixcommitID = sys.argv[1]

command_line = "cd /home/gerope/PhD/EmpiricalStudy/Tokens/nova-token; git checkout p"+fixcommitID+">/dev/null 2>&1; git log -1 | head -1"
output = subprocess.check_output(command_line, shell=True)

tokenCommit = output.split(' ')
tokenCommit = tokenCommit[1].split('\n')
print ("Token Fixed Commit ID:", tokenCommit[0])

webbrowser.open_new_tab('https://github.com/dmgerman/nova-token/commit/'+tokenCommit[0])
webbrowser.open_new_tab('https://github.com/openstack/nova/commit/'+fixcommitID)

command_line = "cd /home/gerope/PhD/EmpiricalStudy/Tokens/nova-token; git log --parents -1 "+tokenCommit[0]+" --oneline | sed -n 1,1p"
token_output = subprocess.check_output(command_line, shell=True)
token_parents = token_output.split('\n')
token_parent = token_parents[0].split(' ')

print ("Token Parent Fix Commit ID:", token_parent[1])

command_line = "cd /home/gerope/PhD/EmpiricalStudy/OpenStack/repositories/nova; git log --parents -1 "+fixcommitID+" --oneline | sed -n 1,1p"
output = subprocess.check_output(command_line, shell=True)
parents = output.split('\n')
parent = parents[0].split(' ')
print ("Nova Parent Fix Commit ID:", parent[1])

file = raw_input("Please enter the file:")
file= file.strip()
webbrowser.open_new_tab('https://github.com/dmgerman/nova-token/blame/'+token_parent[1]+'/'+file)
webbrowser.open_new_tab('https://github.com/openstack/nova/blame/'+parent[1]+'/'+file)
while file !="":
	file = raw_input("Please enter the file:")
	file= file.strip()
	webbrowser.open_new_tab('https://github.com/dmgerman/nova-token/blame/'+token_parent[1]+'/'+file)
	webbrowser.open_new_tab('https://github.com/openstack/nova/blame/'+parent[1]+'/'+file)