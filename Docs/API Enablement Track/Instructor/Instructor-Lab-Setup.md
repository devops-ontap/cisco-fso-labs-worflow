Lab Setup by Instructor/Lab Admin
=================================

Day before Lab
===============

To save time, the day before the lab, the Instructor after each lab will set up the student lab environments. Delete any old student branches from the last lab and create new branches.
Setup is as follows:

Delete any existing git branches
Re-create all git branches from main
Copy lab_vars.py for each branch/az into respective branch and git commit/push
set pipelines for all branches
Unpause pipelines and verify that lab_pre step is green/passes

Stop Here and Proceed to Deploying Lab Overlay Environment
AppD required kube cluster, java app via kube deploy, java app via ec2, load balancer tool deploy

Create new branches with the AZ Name.
=======================================
The us-east-1 region and all AZs are reserved for the lab infra

There is a directory in the git repo called "lab_vars"
There is a directory for each az that is available to use for the student labs.
Copy the lab_vars file for the respective AZ into the corresponding branch 

Example if setting up us-east-2b
==============================
from within the git repo root...

#git checkout -b azname
example:
#git checkout -b us-east-2b

Copy the az lab_vars.py for the az, example, us-east-2b from the lab_vars subdirectory into the root. 
#cp ./lab_vars/us-east-2b .
#git add lab_vars.py 
#git commit -m "added in lab_vars for us-east-2b"
#git push --f


Logon to the concourse team: cisco-fso-labs as administrator. You must be a pipeline administrator to set the pipelines for the team.
Logon-

#fly --target=cisco-fso-lab login --concourse-url=http://ci.devops-ontap.com:8080 -n cisco-fso-labs
This opens your browser URL. Logon with your credentials and paste the bearer token into the command prompt

Set the Pipeline:
If not using the vault you need to set up a parameters file in a directory outside git and pass this command to set the pipeline with the params file:

#fly -t ci set-pipeline -c pipeline-sdwan -p main -l /Users/sconrod/API-Trainings/dev/params/us-east-2a.yml -v aws.region=us-east-2 -v az.name=us-east-2a -v vault.addr=http://prod-vault.devops-ontap.com:8200

If using vault, login to vault with the token provided. First set the following two parameters on your local machine:
VAULT_ADDR=http://vault.devops-ontap.com:8200
VAULT_TOKEN=yourtoken

#vault login

{{UPDATE WITH THE COMMAND TO SET THE PIPELINE AND PASS IN THE VAULT PARAMS}}

Follow these steps to set up all the pipelines for each student.
Once you have set all pipelines you can unpause the pipelines, the lab will automatically deploy for each student but stops before the FSO Agents are installed. WE will leave the install for the lab warm up activity.

Thousand Eyes Console Access for Students
============================================
Student Emails must be added into the Thousand Eyes Lab Console the morning of the lab.
Students will receive an automated email can set their password and login.

The environment will build up to the point where the Thousand Eyes Agents are installed. We have set this as a manual step in order to show students how the agents are deployed.
This is also their first excersize in following the simple workflow.

Student Setup
===============

Students will check out their branch upon starting the lab participation.
They will logon to concourse using via the command line using their branch as their login name. Their password. 

Practise Lab Workflow by Updating and Pushing hostile to git branch
====================================================================
1.add the ip addresses of their ubuntu instances to the hostfile
2.git add, commmit, push the hostfile to their branch

Instructor Knowledge Transfer Thousand Eyes GUI
=====================================================
During this time the Instructor can quickly point out that prior to installing the TE Agents, an OATH key must be created from the TE GUI as well as a group Token.
The OATH token is added to the vault and will be used to run the API commands going forward in the lab by instructor
The Group Token is passed to the AGent Installer Command and is used by the Agents to register to the SAS controller for the lab.


Student Logon to Concourse using Fly
=====================================
1.If the student has not yet installed fly they should do it now. 
The instructor can demonstrate how to do this quickly and paste the steps into the chat
2. student logons to concourse via the command line as follows:
#fly --target=cisco-fso-lab login --concourse-url=http://ci.devops-ontap.com:8080 -n cisco-fso-labs
Their default web browser will open and they will be prompted for their username and password. This is provided via chat to the student by the Instructor
They will paste the token back into the command line of their IDE.

Instructor will demonstrate how to start the job to install the agents, and explain how the job works.
When they start the job, the pipeline pulls the latest commit of the the students git branch and executes the python code via an ephemeral OCI build container.
This OCI build container, was built by the pipeline and has all the correct libraries, python modules to execute the code.
It pulls authenticatation variables from vault, and connects over SSH to the respective EC2 instances and uses a python looping function to install the Thousand Eyes Agents on all the instances.
While the TE Agents are installing, the students can now context switch over to logging into the Thousand Eyes Console and watch for thier agents to appear.

This commences the Part 1 Setup, Workflow, Intro.
Move on to Part 11 - which starts to work with the API and Json and writing python modules to perform automated work against the API for common DEVOPS tasks.









