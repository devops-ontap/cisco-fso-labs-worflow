How to give a team a role:

Step 1: 
Logon to main team as the administrator (ci)

Step 2: 

Create a Team or if Team exists, add role ie):

fly -t $target set-team -n $teamname -c cisco-fso-labs/roles/owner.yml

Step 3:

Logon as the Team

Step 4. Set Pipeline